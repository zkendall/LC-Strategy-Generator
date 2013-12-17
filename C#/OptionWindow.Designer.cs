namespace LCStratGen
{
    partial class OptionWindow
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.ckbx_logging = new System.Windows.Forms.CheckBox();
            this.grpBx_combinations = new System.Windows.Forms.GroupBox();
            this.num_minLoans = new System.Windows.Forms.NumericUpDown();
            this.lbl_gen_minloans = new System.Windows.Forms.Label();
            this.num_Max = new System.Windows.Forms.NumericUpDown();
            this.num_Min = new System.Windows.Forms.NumericUpDown();
            this.lbl_gen_numCombos = new System.Windows.Forms.Label();
            this.lbl_max = new System.Windows.Forms.Label();
            this.lbl_min = new System.Windows.Forms.Label();
            this.ckbx_logSQL = new System.Windows.Forms.CheckBox();
            this.grpBx_combinations.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.num_minLoans)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.num_Max)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.num_Min)).BeginInit();
            this.SuspendLayout();
            // 
            // ckbx_logging
            // 
            this.ckbx_logging.AutoSize = true;
            this.ckbx_logging.Checked = true;
            this.ckbx_logging.CheckState = System.Windows.Forms.CheckState.Checked;
            this.ckbx_logging.Location = new System.Drawing.Point(12, 232);
            this.ckbx_logging.Name = "ckbx_logging";
            this.ckbx_logging.Size = new System.Drawing.Size(100, 17);
            this.ckbx_logging.TabIndex = 0;
            this.ckbx_logging.Text = "Enable Logging";
            this.ckbx_logging.UseVisualStyleBackColor = true;
            this.ckbx_logging.CheckedChanged += new System.EventHandler(this.Logging_CheckedChanged);
            // 
            // grpBx_combinations
            // 
            this.grpBx_combinations.Controls.Add(this.num_minLoans);
            this.grpBx_combinations.Controls.Add(this.lbl_gen_minloans);
            this.grpBx_combinations.Controls.Add(this.num_Max);
            this.grpBx_combinations.Controls.Add(this.num_Min);
            this.grpBx_combinations.Controls.Add(this.lbl_gen_numCombos);
            this.grpBx_combinations.Controls.Add(this.lbl_max);
            this.grpBx_combinations.Controls.Add(this.lbl_min);
            this.grpBx_combinations.Location = new System.Drawing.Point(12, 12);
            this.grpBx_combinations.Name = "grpBx_combinations";
            this.grpBx_combinations.Size = new System.Drawing.Size(270, 119);
            this.grpBx_combinations.TabIndex = 1;
            this.grpBx_combinations.TabStop = false;
            this.grpBx_combinations.Text = "Generator";
            // 
            // num_minLoans
            // 
            this.num_minLoans.Increment = new decimal(new int[] {
            25,
            0,
            0,
            0});
            this.num_minLoans.Location = new System.Drawing.Point(213, 76);
            this.num_minLoans.Maximum = new decimal(new int[] {
            100000,
            0,
            0,
            0});
            this.num_minLoans.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.num_minLoans.Name = "num_minLoans";
            this.num_minLoans.Size = new System.Drawing.Size(51, 20);
            this.num_minLoans.TabIndex = 5;
            this.num_minLoans.Value = new decimal(new int[] {
            100,
            0,
            0,
            0});
            this.num_minLoans.ValueChanged += new System.EventHandler(this.nim_Loans_ValueChanged);
            // 
            // lbl_gen_minloans
            // 
            this.lbl_gen_minloans.AutoSize = true;
            this.lbl_gen_minloans.Location = new System.Drawing.Point(6, 70);
            this.lbl_gen_minloans.MaximumSize = new System.Drawing.Size(170, 0);
            this.lbl_gen_minloans.Name = "lbl_gen_minloans";
            this.lbl_gen_minloans.Size = new System.Drawing.Size(169, 26);
            this.lbl_gen_minloans.TabIndex = 4;
            this.lbl_gen_minloans.Text = "Set the min number of loans a filter set returns to be a viable strategy.";
            // 
            // num_Max
            // 
            this.num_Max.Location = new System.Drawing.Point(213, 38);
            this.num_Max.Maximum = new decimal(new int[] {
            500,
            0,
            0,
            0});
            this.num_Max.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.num_Max.Name = "num_Max";
            this.num_Max.Size = new System.Drawing.Size(51, 20);
            this.num_Max.TabIndex = 3;
            this.num_Max.Value = new decimal(new int[] {
            6,
            0,
            0,
            0});
            this.num_Max.ValueChanged += new System.EventHandler(this.num_Max_ValueChanged);
            // 
            // num_Min
            // 
            this.num_Min.Location = new System.Drawing.Point(213, 12);
            this.num_Min.Maximum = new decimal(new int[] {
            500,
            0,
            0,
            0});
            this.num_Min.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.num_Min.Name = "num_Min";
            this.num_Min.Size = new System.Drawing.Size(51, 20);
            this.num_Min.TabIndex = 3;
            this.num_Min.Value = new decimal(new int[] {
            2,
            0,
            0,
            0});
            this.num_Min.ValueChanged += new System.EventHandler(this.num_Min_ValueChanged);
            // 
            // lbl_gen_numCombos
            // 
            this.lbl_gen_numCombos.AutoSize = true;
            this.lbl_gen_numCombos.Location = new System.Drawing.Point(6, 16);
            this.lbl_gen_numCombos.MaximumSize = new System.Drawing.Size(170, 0);
            this.lbl_gen_numCombos.Name = "lbl_gen_numCombos";
            this.lbl_gen_numCombos.Size = new System.Drawing.Size(156, 26);
            this.lbl_gen_numCombos.TabIndex = 1;
            this.lbl_gen_numCombos.Text = "Set the min and max number of filters per combination.";
            // 
            // lbl_max
            // 
            this.lbl_max.AutoSize = true;
            this.lbl_max.Location = new System.Drawing.Point(183, 40);
            this.lbl_max.Name = "lbl_max";
            this.lbl_max.Size = new System.Drawing.Size(27, 13);
            this.lbl_max.TabIndex = 2;
            this.lbl_max.Text = "Max";
            // 
            // lbl_min
            // 
            this.lbl_min.AutoSize = true;
            this.lbl_min.Location = new System.Drawing.Point(183, 14);
            this.lbl_min.Name = "lbl_min";
            this.lbl_min.Size = new System.Drawing.Size(24, 13);
            this.lbl_min.TabIndex = 2;
            this.lbl_min.Text = "Min";
            // 
            // ckbx_logSQL
            // 
            this.ckbx_logSQL.AutoSize = true;
            this.ckbx_logSQL.Checked = true;
            this.ckbx_logSQL.CheckState = System.Windows.Forms.CheckState.Checked;
            this.ckbx_logSQL.Location = new System.Drawing.Point(118, 232);
            this.ckbx_logSQL.Name = "ckbx_logSQL";
            this.ckbx_logSQL.Size = new System.Drawing.Size(107, 17);
            this.ckbx_logSQL.TabIndex = 2;
            this.ckbx_logSQL.Text = "Log SQL Queries";
            this.ckbx_logSQL.UseVisualStyleBackColor = true;
            this.ckbx_logSQL.CheckedChanged += new System.EventHandler(this.ckbx_logSQL_CheckedChanged);
            // 
            // OptionWindow
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(294, 261);
            this.Controls.Add(this.ckbx_logSQL);
            this.Controls.Add(this.grpBx_combinations);
            this.Controls.Add(this.ckbx_logging);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "OptionWindow";
            this.ShowIcon = false;
            this.SizeGripStyle = System.Windows.Forms.SizeGripStyle.Hide;
            this.Text = "OptionWindow";
            this.grpBx_combinations.ResumeLayout(false);
            this.grpBx_combinations.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.num_minLoans)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.num_Max)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.num_Min)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.CheckBox ckbx_logging;
        private System.Windows.Forms.GroupBox grpBx_combinations;
        private System.Windows.Forms.Label lbl_max;
        private System.Windows.Forms.Label lbl_min;
        private System.Windows.Forms.Label lbl_gen_numCombos;
        private System.Windows.Forms.NumericUpDown num_Min;
        private System.Windows.Forms.NumericUpDown num_Max;
        private System.Windows.Forms.Label lbl_gen_minloans;
        private System.Windows.Forms.NumericUpDown num_minLoans;
        private System.Windows.Forms.CheckBox ckbx_logSQL;
    }
}