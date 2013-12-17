using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace LCStratGen
{
    public partial class OptionWindow : Form
    {
        // Settings Data
        public bool isLogging = true;
        public bool isLogSQL = true;
        public int comb_min = 2;
        public int comb_max = 6;
        public int min_loans = 100;

        public OptionWindow()
        {
            InitializeComponent();
            // Make sure starting values are consistent with code
            ckbx_logging.Checked = isLogging;
            ckbx_logSQL.Checked = isLogSQL;

            num_Min.Value = comb_min;
            num_Max.Value = comb_max;
            num_minLoans.Value = min_loans;
        }

        private void Logging_CheckedChanged(object sender, EventArgs e)
        {
            isLogging = ckbx_logging.Checked;
        }

        private void ckbx_logSQL_CheckedChanged(object sender, EventArgs e)
        {
            isLogSQL = ckbx_logSQL.Checked;
        }

        private void num_Min_ValueChanged(object sender, EventArgs e)
        {
            comb_min = (int)num_Min.Value;
        }

        private void num_Max_ValueChanged(object sender, EventArgs e)
        {
            comb_max = (int)num_Max.Value;
        }

        private void nim_Loans_ValueChanged(object sender, EventArgs e)
        {
            min_loans = (int)num_minLoans.Value;
        }


    }
}
