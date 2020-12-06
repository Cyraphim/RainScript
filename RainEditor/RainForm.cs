using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace RainEditor
{
    public partial class RainForm : Form
    {
        public RainForm()
        {
            InitializeComponent();
        }

        private void richTextBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void richTextBox1_TextChanged_1(object sender, EventArgs e)
        {

        }
        private void OpenDlg()
        {
            OpenFileDialog of = new OpenFileDialog();
            of.Filter = "Text File|*.txt|Any File|*.*";
            if (of.ShowDialog() == DialogResult.OK)
            {
                //open file
                StreamReader sr = new StreamReader(of.FileName);
                //place file text to text box
                fastColoredTextBox1.Text = sr.ReadToEnd();
                
                //close file
                sr.Close();
                //text of this window = path of currently opened file
                this.Text = of.FileName;
            }

        }

        private void openToolStripMenuItem_Click(object sender, EventArgs e)
        {
            OpenDlg();
           

        }

        private void newToolStripMenuItem_Click(object sender, EventArgs e)
        {
            fastColoredTextBox1.Text = "";
        }

        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {
                //save file
                StreamWriter sw = new StreamWriter(this.Text);
                sw.Write(fastColoredTextBox1.Text);
                sw.Close();
            }
            catch
            {
                OpenDlg();
            }
        }
        private void SaveDlg()
        { //new save file dialog
            SaveFileDialog sf = new SaveFileDialog();
            //filter
            sf.Filter = "Text File|*.txt|Any File|*.*";
            //if after showing dialog,user clicked ok
            if (sf.ShowDialog() == DialogResult.OK)
            {
                StreamWriter sr = new StreamWriter(sf.FileName);
                sr.Write(fastColoredTextBox1.Text);
                sr.Close();
            }

        }

        private void saveAsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            SaveDlg();
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void cutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            fastColoredTextBox1. Cut();
        }

        private void copyToolStripMenuItem_Click(object sender, EventArgs e)
        {
            fastColoredTextBox1.Copy();
        }

        private void pasteToolStripMenuItem_Click(object sender, EventArgs e)
        {
            fastColoredTextBox1.Paste();
        }

        private void backgroundColorToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //new color choosing dialog
            ColorDialog cd = new ColorDialog();
            //if after showing dialog,user clicked ok
            if (cd.ShowDialog() == DialogResult.OK)
            {
                //set background color to text box
                fastColoredTextBox1.BackColor = cd.Color;
            }
        }

        private void textColorToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //new color choosing dialog
            ColorDialog cd = new ColorDialog();
            //if after showing dialog,user clicked ok
            if (cd.ShowDialog() == DialogResult.OK)
            {
                //set text color to text box
                fastColoredTextBox1.ForeColor = cd.Color;
            }
        }

        private void fontToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //new font choosing dialog
            FontDialog cd = new FontDialog();
            //if after showing dialog,user clicked ok
            if (cd.ShowDialog() == DialogResult.OK)
            {
                //set font to text box
                fastColoredTextBox1.Font = cd.Font;
            }
        }

        private void undoToolStripMenuItem_Click(object sender, EventArgs e)
        {
            fastColoredTextBox1.Undo();
        }

        private void redoToolStripMenuItem_Click(object sender, EventArgs e)
        {
            fastColoredTextBox1.Redo();
        }

        private void selectAllToolStripMenuItem_Click(object sender, EventArgs e)
        {
            fastColoredTextBox1.SelectAll();
        }

        private void cutToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            fastColoredTextBox1.Cut();
        }

        private void copyToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            fastColoredTextBox1.Copy();
        }

        private void fastColoredTextBox1_Load(object sender, EventArgs e)
        {

        }

        private void pasteToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            fastColoredTextBox1.Paste();

        }

        private void findToolStripMenuItem_Click(object sender, EventArgs e)
        {
            fastColoredTextBox1.ShowFindDialog();
        }

        private void gOTOToolStripMenuItem_Click(object sender, EventArgs e)
        {
            fastColoredTextBox1.ShowGoToDialog();
        }

        private void replaceToolStripMenuItem_Click(object sender, EventArgs e)
        {
            fastColoredTextBox1.ShowReplaceDialog();
        }
    }
}
