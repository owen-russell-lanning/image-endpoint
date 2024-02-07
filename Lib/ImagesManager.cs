namespace ImageEndpoint.Lib
{

    /// <summary>
    /// Used to manage the user's images
    /// </summary>
    public class ImagesManager
    {
        public static ImagesManager Instance;//the current instance of the manager
        private static readonly string IMAGE_FOLDERS_SETTINGS_FILE_PATH = ConfigurationManager.AppSetting["ImageFoldersSettingsFile"];
        private static readonly List<string> SUPPORTED_IMAGE_TYPES = ConfigurationManager.AppSetting["SupportedImageTypes"].Split(",").ToList();

        private List<string> imageFolders = new List<string>();
        

        //path of the daily image and when it was generated
        private string dailyImagePath = null;
        private DateTime dailyImageGenerated = DateTime.Now;


        public ImagesManager()
        {
            ImagesManager.Instance = this;
            InitSettings();

        }


        /// <summary>
        /// creates and initializes any settings or settings file required for the images manager
        /// </summary>
        private void InitSettings()
        {

            //create settings files if they dont exist
            if (!File.Exists(IMAGE_FOLDERS_SETTINGS_FILE_PATH))
            {
                File.Create(IMAGE_FOLDERS_SETTINGS_FILE_PATH).Close();
            }

            //read image folders. each folder is separated by a new line
            string[] untrimmedFolders = File.ReadAllLines(IMAGE_FOLDERS_SETTINGS_FILE_PATH);
            this.imageFolders = new List<string>();
            foreach (string untrimmedFolder in untrimmedFolders)
            {
                var trimmed = untrimmedFolder.Trim();
                if(trimmed.Length == 0 || !Directory.Exists(trimmed))
                {
                    continue;
                }

                this.imageFolders.Add(trimmed);
            }


           
        }


        public string GetRandomImagePath()
        {
            return ImagesManager.GetRandomImagePath(this.imageFolders);
        }


        public string GetDailyImagePath()
        {
            DateTime now = DateTime.Now;
            if(dailyImagePath == null || now.Date.Day != dailyImageGenerated.Date.Day)
            {
                //generate a new daily image
                this.dailyImagePath = GetRandomImagePath();
                this.dailyImageGenerated = now;
            }

            return dailyImagePath;
        }

        /// <summary>
        /// generates a random image recursively from all the folders and image files given to it
        /// <returns>a random image path or null if one cant be found</returns>
        /// </summary>
        private static string GetRandomImagePath(List<string> imageFolders)
        {
            if(imageFolders.Count == 0)
            {
                return null;
            }

            List<int> numsTried = new List<int>();
            string selectedImage = null;
            while(numsTried.Count < imageFolders.Count)
            {
                //generate a random number
                var newRand = Helpers.GenerateRandomIntExcluding(imageFolders.Count, numsTried);
                numsTried.Add(newRand);
                if(newRand == -1)
                {
                    break;
                }

                var selected = imageFolders[newRand];
                if (!Helpers.IsDirectory(selected))
                {
                    selectedImage = selected;
                    break;
                }

                //get all the folders and images in the directory
                List<string> subContent = GetAllFoldersAndImageFiles(selected);
                selectedImage = GetRandomImagePath(subContent);
                if(selectedImage != null)
                {
                    break;
                }

            }

            return selectedImage;
        }



        /// <summary>
        /// 
        /// </summary>
        /// <param name="path"></param>
        /// <returns>a list of all image files and folders in a directory</returns>
        private static List<string> GetAllFoldersAndImageFiles(string path)
        {
            string[] files = Directory.GetFiles(path);
            List<string> outPaths = Directory.GetDirectories(path).ToList();

            foreach(string file in files) {
                if (IsSupportedImageFile(file))
                {
                    outPaths.Add(file);
                }
            }

            return outPaths;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="path"></param>
        /// <returns>true if the given path is a supported image file</returns>
        private static bool IsSupportedImageFile(string path)
        {
            return SUPPORTED_IMAGE_TYPES.Contains(Path.GetExtension(path).ToUpperInvariant());
        }
    }
}
