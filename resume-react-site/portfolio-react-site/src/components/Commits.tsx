import { useEffect, useState } from "react";
import { fetchCommits } from "../utils/FetchCommits";

function Commits() {
  const [commits, setCommits] = useState([]);
  const repoOwner = "raypoci";
  const repoName = "raypoci.github.io";

  useEffect(() => {
    async function getCommits() {
      const commitData = await fetchCommits({
        repoOwner: repoOwner,
        repoName: repoName,
      });
      setCommits(commitData);
    }
    getCommits();
  }, [repoOwner, repoName]);

  console.log(commits);
  return (
    <div>
      <h1>Recent Commits</h1>
      <ul>test</ul>
    </div>
  );
}

export default Commits;
