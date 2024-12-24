import axios from "axios";

export interface Commit {
  commit: {
    author: {
      date: string;
    };
  };
}

// Fetch commits from GitHub
export const fetchCommits = async (): Promise<Commit[]> => {
  try {
    const response = await axios.get<Commit[]>(
      "https://api.github.com/repos/raypoci/raypoci.github.io/commits"
    );
    console.log("Fetched Data:", response.data); // Debugging log
    return response.data;
  } catch (error) {
    console.error("Error fetching commits:", error);
    return [];
  }
};
