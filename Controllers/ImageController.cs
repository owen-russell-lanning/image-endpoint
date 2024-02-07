using ImageEndpoint.Lib;
using Microsoft.AspNetCore.Hosting.Server;
using Microsoft.AspNetCore.Mvc;

namespace ImageEndpoint.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class ImageController : Controller
    {

        /// <summary>
        /// gets today image. each day, a new image is selected from the folders
        /// </summary>
        /// <returns>the daily image</returns>
        [HttpGet]
        [Route("Today")]
        public ActionResult GetTodaysImage()
        {
            var selected = ImagesManager.Instance.GetDailyImagePath();
            return PhysicalFile(selected, "image/jpeg");
        }
    }
}
