using System;
using EasyTabs;


namespace RainEditor
{
    public partial class AppContainer : TitleBarTabs
    {
        public AppContainer()
        {
            InitializeComponent();
            AeroPeekEnabled = true;
            TabRenderer = new ChromeTabRenderer(this);

        }
        public override TitleBarTab CreateTab()

        {
            return new TitleBarTab(this)
            {
                Content = new RainForm
                {
                    Text = "New Tab"
                }


            };
            throw new NotImplementedException();
        }
        private void AppContainer_Load(object sender, EventArgs e)
        {

        }
    }
}
