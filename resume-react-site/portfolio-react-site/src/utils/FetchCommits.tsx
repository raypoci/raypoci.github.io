import axios from "axios";

export interface Commit {
  commit: {
    author: {
      date: string;
    };
  };
  repository?: string;
}

export interface RepoConfig {
  owner: string;
  name: string;
  isPrivate?: boolean;
}

// Fetch commits for a single repository
const fetchRepoCommits = async (
  repo: RepoConfig,
  token?: string
): Promise<Commit[]> => {
  try {
    const headers: Record<string, string> = {};
    if (token && repo.isPrivate) {
      headers.Authorization = `token ${token}`;
    }

    const response = await axios.get<Commit[]>(
      `https://api.github.com/repos/${repo.owner}/${repo.name}/commits`,
      { headers }
    );

    return response.data.map((commit) => ({
      ...commit,
      repository: `${repo.owner}/${repo.name}`,
    }));
  } catch (error) {
    console.error(
      `Error fetching commits for ${repo.owner}/${repo.name}:`,
      error
    );
    return [];
  }
};

// Fetch commits from multiple GitHub repositories
export const fetchCommits = async (
  repos: RepoConfig[],
  token?: string
): Promise<Commit[]> => {
  try {
    // Fetch commits for all repositories in parallel
    const commitPromises = repos.map((repo) => fetchRepoCommits(repo, token));
    const repoCommits = await Promise.all(commitPromises);

    // Combine and sort all commits by date
    const allCommits = repoCommits
      .flat()
      .sort(
        (a, b) =>
          new Date(b.commit.author.date).getTime() -
          new Date(a.commit.author.date).getTime()
      );

    return allCommits;
  } catch (error) {
    console.error("Error fetching commits:", error);
    return [];
  }
};
