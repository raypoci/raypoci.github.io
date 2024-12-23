interface FetchCommitsProps {
  repoOwner?: string;
  repoName?: string;
}

export async function fetchCommits({
  repoOwner = "raypoci",
  repoName = "raypoci.github.io",
}: FetchCommitsProps) {
  const url = `https://api.github.com/repos/${repoOwner}/${repoName}/commits`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const commits = await response.json();
    return commits;
  } catch (error) {
    console.error("Error fetching commits:", error);
    return [];
  }
}
