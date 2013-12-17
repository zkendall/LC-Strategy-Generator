/*
 * Zachariah Kendall
 * Nov-Dec 2013
 *  
 * [LOG]:
 *      Nov *:  Put in database (init and data loading) and gui (menus, tree view and options)
 *      Dec 2:  Got selected filters appropriatly translating to sql
 *      Dec 4:  Found 3rd party combination library. Implemented.
 *              Got a logging system going, with menus to view and clear.
 *              Added options window.
 *      Dec 5:  Executing queries in bulk now.
 *              But realized I should populate a table with reaults instead, less transaction overhead
 *              Dealing with errors :(
 *      Dec 6:  Got a progress bar going.
 *              Other tweaking.
 *      Dec 7:  Got semi-workable ROI. Still not great, but it's something.
 *              Moving processing to background thread, so progress bar can render cleanly.
 *              Added functionality to qualify strat sets by loan count.
 *              Found and diagnosed duplicate problem... Not sure how/when to proceed on that.
 *      Dec 8:  
 *              Learning more about different available data files and columns.
 *              Adding more columns and filter options.
 *              Added bg worker for import csv 
 *              Finally implementing the static tree...and handling the resulting problems.
 *              Woooosta!
 *      
 * 
 * [TO DO]: 
 * MUST:
 *      -Implement tmp table from which to select combos from
 *      -I'M HAVING A DUPLICATE PROBLEM!
 *          Diagnosis: When more than 2 options of the same filter are combined,
 *          my WHERE is reducing them to min and max.
 *              Shit. I think I'll have to edit the comination algorithm to treat
 *              certain types of filters as if the k-value is always 2. Humm...
 * Small:
 *      Need to pull from options datatags too, not just filters.
 *          Is this needed? I got it working without.
 *      Handle bg thread cancelation.
 *      Set min requied results per query to qualify as viable strategy.
 *      Change how results are shown to user..
 *      Keep list of indexes of top 10 queries.
 *      Set min/max filter sets to default to 0-V, if user selects only 1 option.
 *      Put in more useful filters.
 *      Have select ALL/NON options
 *      Be able to save settings & tree selection in db.
 *      
 * Big:
 *      Figure out what to do about memory for large combination sets.
 *           Don't want to keep 100s of mbs of sql in memory waiting to be executed...
 *           Demp to and read from flat file?
 *      Data visualization: Charting loan performance over time. 
 *      Use A* algorithm to guide combinator? This will make large numbers of filters feasible.
 *      
 * 
 * Future:
 *      Sexier filter menus instead of check-box tree.
 *      Ran into "Loans that do not meet the credit policy" seperator in data file. How to handle?
 *          Removed for now. Future: implement setting which will require parsing status after hitting that flag.
 * 
 * 
 */

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

// Third party includes
using Facet.Combinatorics;


namespace LCStratGen
{
    public partial class MainWindow : Form
    {
        // Data members
        Database db;
        public OptionWindow w_options;
        public ProgressWindow w_progress;
        System.IO.StreamWriter m_log;
        List<string> m_generated_queries;
        List<Tuple<int, double, int>> m_generated_results;

        // Settings
        bool logging = true;
        string LOG_FILE_NAME = "log.txt";

        public MainWindow()
        {
            // Connect to log. Append.
            m_log = new System.IO.StreamWriter(LOG_FILE_NAME, true);
            m_log.AutoFlush = true;
            db = new Database(this);
            m_generated_queries = new List<string>();

            InitializeComponent();
            this.bgWorker_import.DoWork += new System.ComponentModel.DoWorkEventHandler(this.db.importCSV);
            w_options = new OptionWindow();
            w_progress = new ProgressWindow();
            w_progress.StartPosition = FormStartPosition.CenterParent;


        }

        /*
         * Import CSV file
         */
        private void Menu_LoadHistory_Click(object sender, EventArgs e)
        {
            OpenFileDialog dlg_openFile = new OpenFileDialog();
            dlg_openFile.Filter = "CSV files (*.csv)|*.csv|All files (*.*)|*.*";
            if (dlg_openFile.ShowDialog() == DialogResult.OK)
            {
                if (bgWorker_gen.IsBusy != true)
                {
                    bgWorker_import.RunWorkerAsync(dlg_openFile.FileName);
                    // Progress Bar
                    w_progress.bar.Value = 0;
                    w_progress.message.Text = "Importing CSV...";
                    w_progress.Show();
                }
            }
        }

        /*
         * Activate generator in background worker
         */
        private void Menu_Generate_Click(object sender, EventArgs e)
        {
            // Run Generate() in seperate thread
            if (bgWorker_gen.IsBusy != true)
            {
                textBox.Text = "";
                bgWorker_gen.RunWorkerAsync();
                generateMenuItem.Text = "Cancle Run";
                // Show progress bar
                w_progress.bar.Value = 0;
                w_progress.Show(this);
                w_progress.message.Text = "Generating Combinations...";
            }
            else
            {
                bgWorker_gen.CancelAsync();
                generateMenuItem.Text = "Generate";
                w_progress.Hide();
            }
        }


        /*
         * Starting point for the stategy generation algorithm
         */
        private void Generate(object sender, DoWorkEventArgs eArgs)
        {
            BackgroundWorker worker = sender as BackgroundWorker;

            // Get filters and options
            List<Tuple<string, string>> staticSet = Get_Tree_Options(tree_Static);
            List<Tuple<string, string>> iterSet = Get_Tree_Options(tree_Iterate);

            // Use static list to create temporary table
            string queryBase = "INSERT INTO tmp SELECT * FROM loan WHERE ";
            string query = db.buildFilterQuery(queryBase, staticSet);
            log("Static query: " + query);

            // Create temporary table to query from
            db.make_loan_table("tmp", true);
            db.execute_nonquery(query);

            // Disable autoflush for heavy logging
            m_log.AutoFlush = false;

            // Base for generated queries
            queryBase = "INSERT INTO roi (avg_roi, count)"
                                + " SELECT IFNULL(avg(roi), 0), count(id)"
                                + " FROM tmp WHERE ";

            log("Generating combinations...");
            Combinations<Tuple<string, string>> combinations;
            for (int i = w_options.comb_min; i < w_options.comb_max; i++)
            {                
                combinations = new Combinations<Tuple<string, string>>(iterSet, i);

                log("Selecting "+i+" filters, there are "+combinations.Count+" combinations of selected filters.", false);

                foreach (List<Tuple<string, string>> combo in combinations)
                {
                    query = db.buildFilterQuery(queryBase, combo);
                    if (query == "")
                        continue;
                    m_generated_queries.Add(query);
                    if(w_options.isLogSQL)
                        log(query, false);
                }

                double percent = (double)(i+1 - w_options.comb_min) / (double)(w_options.comb_max - w_options.comb_min);
                worker.ReportProgress((int)(percent * 100));
                m_log.Flush();
            } // END COMBINATING FORLOOP
            
            // Re-enable normal flushing
            m_log.AutoFlush = true;
            log("Finished generating combinations.");

            // Execute generated sql
            m_generated_results = db.query_bulk_roi(worker, eArgs, m_generated_queries);

        } // End Generate()

        /*
         * Show the results of a generator run
         */
        private void showResults()
        {
            // Temporary: Show ROI and strategy results
            // TODO: do better!

            if (m_generated_queries.Count == 0)
            {
                textBox.Text = "No results.\nTry expanding your filter set or make sure the database is loaded.";
                return;
            }

            foreach (Tuple<int, double, int> r in m_generated_results)
            {
                string q = m_generated_queries.ElementAt(r.Item1 - 1);
                string strat = q.Remove(0, q.IndexOf("WHERE")+5);
                textBox.AppendText("ROI: " + r.Item2 * 100 + "% From: " + r.Item3 + " loans" + Environment.NewLine);
                textBox.AppendText("Stragegy: " + strat + Environment.NewLine + Environment.NewLine);
            }
        }

        /*
         * Generator Background Worker: update progess
         */ 
        private void backgroundWorker_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            w_progress.bar.Value = e.ProgressPercentage;
        }

        /*
         * Generator Background Worker: completed
         */
        private void backgroundWorker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            showResults();
            generateMenuItem.Text = "Generate";
            w_progress.bar.Value = 0;
            w_progress.Hide();
        }

        /*
         * Import CSV Background Worker: update progress
         */ 
        private void bgWorker_import_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            w_progress.bar.Value = e.ProgressPercentage;
        }

        /*
         * Import CSV Background Worker: completed
         */ 
        private void bgWorker_import_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            w_progress.bar.Value = 0;
            w_progress.Hide();
        }

        /*
         * Return the options selected in a TreeView in the form of a List of Tuples
         */
        private List<Tuple<string, string>> Get_Tree_Options(TreeView tree)
        {
            log("Getting tree options from: "+tree.Name);
            List<Tuple<string, string>> filters = new List<Tuple<string, string>>();

            // Iterate through filters
            foreach (TreeNode n in tree.Nodes)
            {
                if (n.Checked)
                {
                    log("Node checked: " + n.Name);
                    // Iterate through filter's options
                    foreach (TreeNode o in n.Nodes)
                    {
                        if (o.Checked)
                            filters.Add(new Tuple<string, string>(n.Tag.ToString(), o.Tag.ToString()));
                    }
                }
            }
            return filters;
        }

        /*
         * Show Options window.
         */ 
        private void optionsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            w_options.ShowDialog();
            logging = w_options.isLogging;
        }

        /*
         * Maintain a log file instead of console as it is much faster.
         */
        public void log(string msg, bool close=true)
        {
            if(!logging)
                return;

            // Is log closed?
            if (m_log == null || m_log.BaseStream == null)
            {
                try
                {
                    m_log = new System.IO.StreamWriter(LOG_FILE_NAME, true);
                }
                catch (Exception e) { Console.WriteLine("Could not open log: " + e.Message); }
            }

            m_log.WriteLine(msg);

            if(close)
                m_log.Close();
        }

        /*
         * Main window cleanup.
         */
        private void MainWindow_FormClosing(object sender, FormClosingEventArgs e)
        {
            // Make sure the log is closed.
            m_log.Dispose();
        }

        /*
         * Open log via system default
         */
        private void openLogToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Process.Start(LOG_FILE_NAME);
        }

        /*
         * Delete the log file
         */
        private void clearLogToolStripMenuItem_Click(object sender, EventArgs e)
        {
            m_log.Close();
            m_log = new System.IO.StreamWriter(LOG_FILE_NAME, false);
        }

    }
}
