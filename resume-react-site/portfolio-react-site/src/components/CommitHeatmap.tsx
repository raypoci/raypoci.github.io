import React, { useEffect, useState } from "react";
import axios from "axios";
import CalendarHeatmap from "react-calendar-heatmap";
import "react-calendar-heatmap/dist/styles.css";
import moment from "moment";

// Define types for commit data
interface Commit {
  commit: {
    author: {
      date: string;
    };
  };
}

// Fetch commits from GitHub
const fetchCommits = async (): Promise<Commit[]> => {
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

const CommitHeatmap: React.FC = () => {
  const [commits, setCommits] = useState<Commit[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchCommits();
      setCommits(data);
    };
    fetchData();
  }, []);

  // Grouping commits by date and counting them
  const groupedCommits = commits.reduce(
    (acc: Record<string, number>, commit: Commit) => {
      const date = moment(commit.commit.author.date).format("YYYY-MM-DD");
      acc[date] = (acc[date] || 0) + 1;
      return acc;
    },
    {}
  );

  // Format data for react-calendar-heatmap
  const heatmapData = Object.keys(groupedCommits).map((date) => ({
    date: date,
    count: groupedCommits[date],
  }));

  console.log("Heatmap Data:", heatmapData); // Debugging log
  const startDate = moment("2020-08-01").toDate();
  console.log(startDate);
  return (
    <div>
      <h2>Commit Activity Heatmap</h2>
      <CalendarHeatmap
        startDate={startDate}
        endDate={moment().subtract(4, "year").toDate()}
        values={heatmapData}
        classForValue={(value) => {
          if (!value) {
            return "color-empty";
          }
          return `color-github-${Math.min(4, Math.ceil(value.count / 2))}`;
        }}
        showWeekdayLabels
      />
    </div>
  );
};

export default CommitHeatmap;
