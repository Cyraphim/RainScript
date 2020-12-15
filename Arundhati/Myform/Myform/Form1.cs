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


namespace Myform
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        Stream myStream;
        private void treeView1_AfterSelect(object sender, TreeViewEventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.Hide();
            Form2 f2 = new Form2();
            f2.Show();
        }
        
        private void openToolStripMenuItem_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();

            ofd.Filter = "gpd|*.rain";
            
            if(ofd.ShowDialog()== DialogResult.OK)
            {
                if ((myStream == ofd.OpenFile())!=null)
                {


                    string strfilename = ofd.FileName;
                    string filetext = File.ReadAllText(strfilename);
                    GetRichTextBox().Text = filetext;
                }

                    
                    

            }

        }
        private RichTextBox GetRichTextBox()
        {
            RichTextBox rtb = null;
            TabPage tp = tabControl1.SelectedTab;
            if(tp != null)
            {
                rtb = tp.Controls[0] as RichTextBox;
            }
            return rtb;
        }


        private void newToolStripMenuItem_Click(object sender, EventArgs e)
        {
            TabPage tp = new TabPage("New Tab");
            RichTextBox rtb = new RichTextBox();
            rtb.Dock = DockStyle.Fill;
            tp.Controls.Add(rtb);

            tabControl1.TabPages.Add(tp);
            

        }

        private void cutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            GetRichTextBox().Cut();
        }

        private void copyToolStripMenuItem_Click(object sender, EventArgs e)
        {
            GetRichTextBox().Copy();

        }

        private void pasteToolStripMenuItem_Click(object sender, EventArgs e)
        {
            GetRichTextBox().Paste();

        }

        private void toolStripButton1_Click(object sender, EventArgs e)
        {
            TabPage current_tab = tabControl1.SelectedTab;
            tabControl1.TabPages.Remove(current_tab);
        }
        



        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            DialogResult dialog = MessageBox.Show("do you really want to exit?", "Exit", MessageBoxButtons.YesNo);
            if(dialog==DialogResult.Yes)
            {
                Application.ExitThread();
            }
            else if(dialog==DialogResult.No)
            {
                e.Cancel = true;
            }
        }



    }
}
