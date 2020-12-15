using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.Win32;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using EasyTabs;

namespace RainEditor
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            AppContainer container = new AppContainer();
            //add initial tab
            container.Tabs.Add(
                new TitleBarTab(container)
                {
                    Content = new RainForm
                    {
                        Text = " New Tab"
                    }
                }
                );

            //set initial tab the first one
            container.SelectedTabIndex = 0;
            //create tabs and start application
            TitleBarTabsApplicationContext applicationContext = new TitleBarTabsApplicationContext();
            applicationContext.Start(container);
            Application.Run(applicationContext);

           
        }
      
    }

}
