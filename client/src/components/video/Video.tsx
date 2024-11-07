import HeroVideoDialog from "@/components/ui/hero-video-dialog";
function Video() {
  return (
    <div className="relative">
    <HeroVideoDialog
      animationStyle="from-bottom"
      videoSrc="http://localhost:8000/api/v1/video"
      thumbnailSrc="./bg.png"
      thumbnailAlt="Hero Video"
    />
  </div>
  )
}

export default Video