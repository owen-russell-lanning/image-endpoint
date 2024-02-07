namespace ImageEndpoint.Lib
{
    /// <summary>
    /// Misc helpers
    /// </summary>
    public class Helpers
    {

        /// <summary>
        /// generates a random int excluding the list given
        /// </summary>
        /// <param name="max">number to generate less than<param>
        /// <param name="exclude">list of ints to exclude</param>
        /// <returns>random int or -1 if one cannot be generated</returns>
        public static int GenerateRandomIntExcluding(int max, IEnumerable<int> exclude)
        {
            if(max == exclude.Count())
            {
                return -1;
            }

            Random rng = new Random();
            int currentRand = rng.Next(max);
            while (exclude.Contains(currentRand))
            {
                currentRand = rng.Next(max);
            }

            return currentRand;
        }


        /// <summary>
        /// checks if a path is a directory
        /// </summary>
        /// <param name="path"></param>
        /// <returns>true if the given path is a directory</returns>
        public static bool IsDirectory(string path){
            FileAttributes attr = File.GetAttributes(path);

            //detect whether its a directory or file
            return ((attr & FileAttributes.Directory) == FileAttributes.Directory);

        }
    }
}
