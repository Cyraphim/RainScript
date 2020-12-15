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
    public partial class Form2 : Form
    {
        List<string> listFiles = new List<string>();
        public Form2()
        {
            InitializeComponent();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void listView1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            listFiles.Clear();
            listView1.Items.Clear();
            using(FolderBrowserDialog fbd= new FolderBrowserDialog() { Description= "Select your path."})
            {
                if(fbd.ShowDialog()==DialogResult.OK)
                {
                    textBox1.Text = fbd.SelectedPath;
                    foreach(string item in Directory.GetFiles(fbd.SelectedPath))
                    {
                        imageList1.Images.Add(System.Drawing.Icon.ExtractAssociatedIcon(item));
                        FileInfo fi = new FileInfo(item);
                        listFiles.Add(fi.FullName);
                        listView1.Items.Add(fi.Name, imageList1.Images.Count);

                    }

                }
            }
        }
    }
}
