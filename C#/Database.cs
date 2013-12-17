using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Threading.Tasks;
using System.Data.SQLite;
using System.Windows.Forms;
using System.Text.RegularExpressions;
using System.ComponentModel;

namespace LCStratGen
{
    class Database
    {
        // Properties
        string LOG_FILE_NAME = "history.db";

        // Members
        MainWindow w_main;
        SQLiteConnection gl_db;
        Random rand;

        // Filter Delegates
        public delegate string filterHandler(TreeNode node);

        /*
         * Constructor
         */
        public Database(MainWindow main)
        {
            initialize();
            rand = new Random();
            w_main = main;
        }

        /*
         * Handle building queries 
         */
        public string buildFilterQuery(string queryBase, List<Tuple<string, string>> filters)
        {
            // Query base without WHERE-clause
            string query = queryBase;

            List<string> wheres = new List<string>();

            // Build option groupings by filter name
            var filterGroups =
                from f in filters
                group f.Item2 by f.Item1 into g
                select new { Filter = g.Key, Options = g };

            // Process each grouping to build appropriate WHERE segment
            foreach (var g in filterGroups)
            {
                List<string> options = new List<string>();
                foreach (var o in g.Options)
                    options.Add(o);

                // Add WHERE criteria to list
                wheres.Add(build_WHERE_Clause(g.Filter, options));
            }

            if (wheres.Count < 1)
                return "";

            // Add WHERE-sql to query
            query += String.Join(" AND ", wheres);

            return query;
        }

        /*
         *  Pass data to appropriate WHERE-clause builder
         */
        public string build_WHERE_Clause(string filter, List<string> options)
        {
            string result = "";
            // Switch filter type
            switch (filter)
            {
                case "loan_amnt":
                case "annual_inc":
                    result = _WHERE_min_max(filter, options);
                    break;
                case "term":
                case "grade":
                case "emp_length":
                case "home_ownership":
                case "purpose":
                    result = _WHERE_in(filter, options);
                    break;
            }
            // Send options to aux function based on type

            return result;
        }

        /*
         *  Axillary method for build_WHERE_Clause()
         *  Build sql-WHERE clause with BETWEEN the min and max values in options
         */
        public string _WHERE_min_max(string attribute, List<string> options)
        {
            // TODO: Handle only one option. Select from zero-to-option?

            string where = "";
            if (options[0].Contains('.'))
            {   // Convert to list of doubles
                List<double> l = new List<double>();
                foreach (string s in options)
                    l.Add(double.Parse(s));

                where = attribute + " BETWEEN " + l.Min() + " AND " + l.Max();
            }
            else
            {   // Convert to list of integers
                List<double> l = new List<double>();
                foreach (string s in options)
                    l.Add(double.Parse(s));

                where = attribute + " BETWEEN " + l.Min() + " AND " + l.Max();
            }

            return where;
        }

        /*
         *  Axillary method for build_WHERE_Clause()
         *  Build sql-WHERE clause with [attribute IN (o1, o2, etc)]
         */
        public string _WHERE_in(string attribute, List<string> options)
        {
            string where = attribute + " IN (\"" + string.Join("\", \"", options) + "\")";
            return where;
        }

        /*
         * Execute a list of SQL select queries
         */
        public List<Tuple<int, double, int>> query_bulk_roi(BackgroundWorker worker, DoWorkEventArgs eArgs, List<string> queries)
        {
            List<Tuple<int, double, int>> results = new List<Tuple<int, double, int>>();

            w_main.log("Executing generated queries to get average ROI.");
            // Refresh progress bar for this job
            worker.ReportProgress(0);

            // Remove previous ROI results
            remake_roi_table(true);

            gl_db.Open();
            using (var cmd = new SQLiteCommand(gl_db))
            using (var transaction = gl_db.BeginTransaction())
            {
                for(int i = 0; i < queries.Count; i++)
                {
                    cmd.CommandText = queries[i];
                    try
                    {
                        cmd.ExecuteNonQuery();
                    }
                    catch (Exception e) { Console.WriteLine(e); }
                    int percent = (int) (((double)i / (double)queries.Count)*100);
                    worker.ReportProgress(percent);
                    // Check for cancelation
                    if ((worker.CancellationPending == true))
                    {
                        eArgs.Cancel = true;
                        return results;
                    }
                }
                // TODO: I tmp hangs in commmit. Communicate action to user...
                transaction.Commit();
            }

            // Get results table
            using (var cmd = new SQLiteCommand(gl_db))
            {
                // Select top 10 performers that meet user criteria
                cmd.CommandText = "SELECT id, avg_roi, count FROM roi WHERE count >= " + w_main.w_options.min_loans
                                + " ORDER BY avg_roi desc LIMIT 10";
                SQLiteDataReader rd = cmd.ExecuteReader();
                while (rd.Read())
                    results.Add(new Tuple<int, double, int>(rd.GetInt32(0), rd.GetDouble(1), rd.GetInt32(2)));
            }
            gl_db.Close();
            w_main.log("Finished executing generated queries.");
            return results;
        }

        /*
         * Open CSV file and insert into db
         */
        public void importCSV(object sender, DoWorkEventArgs eArgs)
        {
            BackgroundWorker worker = sender as BackgroundWorker;
            string fileName = (string)eArgs.Argument;
            string line, query;

            // Clean import?
            DialogResult res = MessageBox.Show("Delete existing database first?", "Database", MessageBoxButtons.YesNo);
            if (res == DialogResult.Yes)
                make_loan_table("loan", true);

            // Process CSV
            gl_db.Open();
            using (StreamReader fin = File.OpenText(fileName))
            using (var cmd = new SQLiteCommand(gl_db))
            using (var transaction = gl_db.BeginTransaction())
            {
                // Count lines for progress bar...
                int count = 0;
                while (!fin.EndOfStream)
                {
                    fin.ReadLine();
                    count++;
                }
                fin.BaseStream.Seek(0, 0); // Return to beginning.

                // Skip header
                fin.ReadLine();
                fin.ReadLine();

                // Get logged saved as sql in queue
                int i = 0;
                while (!fin.EndOfStream)
                {
                    i++;
                    line = fin.ReadLine();
                    if (line == "")
                        continue;

                    // Clean string
                    line = line.Remove(0, 1); // Initial quotation-mark
                    line = line.Replace('\'', ' '); // Single quotes in text
                    String[] values = Regex.Split(line, "\",\""); // Split on:  ","

                    // Don't include unfinished loans by checking 'loan_status'
                    if (values[19] == "Current")
                        continue;

                    // Formated 5 per line for readability
                    query = String.Format("INSERT INTO loan ("
                        + "id, loan_amnt, term, grade, emp_length, "
                        + "home_ownership, annual_inc, issue_d, loan_status, purpose, "
                        + "total_pymnt, total_pymnt_inv, total_rec_prncp, total_rec_int, roi "
                        +") "

                        + "values (  '{0}', '{1}', '{2}', '{3}', '{4}', "
                        + "'{5}', '{6}', '{7}', '{8}', '{9}', "
                        + "'{10}', '{11}', '{12}', '{13}', {14} )"

                        , values[0], values[2], values[5], values[8], values[11]
                        , values[12], values[13], values[18], values[19], values[23]
                        , values[55], values[56], values[57], values[58], Get_ROI(values)
                    ); // END query
                    cmd.CommandText = query;
                    try
                    {
                        cmd.ExecuteNonQuery();
                    }
                    catch (Exception ex) { Console.WriteLine(ex); }

                    // Update progress bar
                    double percent = (double)i/count;
                    worker.ReportProgress((int)(percent * 100));

                } // END WHILE
                transaction.Commit();
            } // END USING
            gl_db.Close();
        } // END importCSV()

        /*
         * Calculate the ROI
         */
        private double Get_ROI(string[] values)
        {
            // TODO: Refine this...

            string total_pymnt = values[55];
            string loan_amnt = values[2];

            // Validity check
            if (total_pymnt == "" || loan_amnt == "")
                return 0.0;

            return double.Parse(total_pymnt) / int.Parse(loan_amnt) - 1;
        }

        /*
         * Populate tmp table
         */
        public void execute_nonquery(string query)
        {
            gl_db.Open();

            using (var cmd = new SQLiteCommand(gl_db))
            {

                cmd.CommandText = query;
                cmd.ExecuteNonQuery();
            }
            gl_db.Close();
        }

        /*
         * Create ROI table
         */
        private void initialize()
        {
            try
            {
                gl_db = new SQLiteConnection("Data Source=" + LOG_FILE_NAME);
                make_loan_table("loan", false);
                make_loan_table("tmp", false);
                remake_roi_table(true);
            }
            catch (Exception e)
            {
                MessageBox.Show(e.Message);
            }
        }

        /*
         * Create loan table
         */
        public void make_loan_table(string name, bool drop)
        {
            gl_db.Open();

            using (var cmd = new SQLiteCommand(gl_db))
            {
                if (drop)
                {
                    cmd.CommandText = "DROP TABLE IF EXISTS " + name;
                    cmd.ExecuteNonQuery();
                }
                // Loan table
                cmd.CommandText = "CREATE TABLE IF NOT EXISTS " + name +
                                    "(id INTEGER NOT NULL PRIMARY KEY," +
                                    "roi REAL," +
                                    "loan_amnt INTEGER," +
                                    "term TEXT," +
                                    "grade TEXT," +
                                    "emp_length TEXT," +
                                    "home_ownership TEXT," +
                                    "annual_inc INTEGER," +
                                    "issue_d TEXT," +
                                    "loan_status TEXT," +
                                    "purpose TEXT," +
                                    "total_pymnt REAL," +
                                    "total_pymnt_inv REAL," +
                                    "total_rec_prncp INTEGER," +
                                    "total_rec_int REAL" +
                                    ")";
                cmd.ExecuteNonQuery();
            }
            gl_db.Close();
        }

        /*
         * Create ROI table
         */
        public void remake_roi_table(bool drop)
        {
            gl_db.Open();
            using (var cmd = new SQLiteCommand(gl_db))
            {
                if (drop)
                {// Remove previous results
                    cmd.CommandText = "DROP TABLE IF EXISTS roi";
                    cmd.ExecuteNonQuery();
                }

                // Average ROI results table
                cmd.CommandText = "CREATE TABLE IF NOT EXISTS roi (" +
                                    "id INTEGER NOT NULL PRIMARY KEY," +
                                    "avg_roi REAL," +
                                    "count INT)";
                cmd.ExecuteNonQuery();
            }
            gl_db.Close();
         
        }
    }// END CLASS

}//END NAMESPACE
