import Video from "../video/Video";
export default function Home() {
  return (
    <section className="Home py-10 px-4" id="Home">
      <h2 className="text-3xl">VideoDialog</h2>
      <br />
      <div id="video" className="grid grid-cols-3 gap-4">
        <div id="divece-x">
          <Video />
        </div>
      </div>
    </section>
  );
}
