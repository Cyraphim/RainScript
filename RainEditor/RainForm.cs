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
using EasyTabs;



namespace RainEditor
{
    public partial class RainForm : Form
    {
        protected TitleBarTabs ParentTabs
        {
            get
            {
                return (ParentForm as TitleBarTabs);
            }
        }
        string CurrentFileName;
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
            of.Filter = "RainScript File|*.rain";
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


        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            
            try
            {
                if (this.Text == "Rain Editor")
                {
                    throw new Exception(" Go to Save Dialog");
                }
                //save file
                StreamWriter sw = new StreamWriter(this.Text);
                sw.Write(fastColoredTextBox1.Text);
                sw.Close();
            }
            catch
            {
                SaveDlg();
            }
        }
        private void SaveDlg()
        { //new save file dialog
            SaveFileDialog sf = new SaveFileDialog();
            //filter
            sf.Filter = "RainScript File|*.rain";
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

        private void RainForm_Load(object sender, EventArgs e)
        {
            this.KeyPreview = true;
        }

        private void editToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void fileToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void openFileInNewTabToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void treeView1_AfterSelect(object sender, TreeViewEventArgs e)
        {

        }
        String Path = "C:\\Users\\Rheya Dhar\\Desktop\\rain files";

       
        
       
        private void newToolStripMenuItem_Click(object sender, EventArgs e)
        {
            TabPage tp = new TabPage("NEW DOCUMENT");
           RichTextBox rtb = new RichTextBox();
            rtb.Dock = DockStyle.Fill;
            tp.Controls.Add(rtb);
            tabControl1.TabPages.Add(tp);

            
          

        }
        //save ctrl+s and open ctrl+O
        private void RainForm_KeyDown(object sender, KeyEventArgs e)
        {
            if(e.Control== true && e.KeyCode== Keys.S)
            {
                saveToolStripMenuItem.PerformClick();
            }
            if (e.Control == true && e.KeyCode == Keys.O)
            {
                openToolStripMenuItem.PerformClick();
            }
            if (e.Control == true && e.Shift==true && e.KeyCode == Keys.S)
            {
                saveAsToolStripMenuItem.PerformClick();
            }
            if (e.Control == true && e.KeyCode == Keys.E)
            {
                exitToolStripMenuItem.PerformClick();
                
            }
        }
        //final exit form
        private void RainForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            try
            {
                DialogResult dialog = MessageBox.Show("Do you really want to close the program?", "Exit", MessageBoxButtons.YesNo);
                if (dialog == DialogResult.Yes)
                {
                    Application.ExitThread();

                }
                else if (dialog == DialogResult.No)
                {
                    e.Cancel = true;
                }


            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }

        }

        private void tabControl1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }
    }
}
