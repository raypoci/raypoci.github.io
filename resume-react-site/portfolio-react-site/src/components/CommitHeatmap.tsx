import React, { useEffect, useState } from "react";
import axios from "axios";
import CalendarHeatmap from "react-calendar-heatmap";
import "react-calendar-heatmap/dist/styles.css";
import moment from "moment";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import "../App.css"; // Ensure the path is correct

// Define types for commit data
interface Commit {
  commit: {
    author: {
      date: string;
    };
  };
}

type HoverValue = { date: string; count?: number } | null;

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

  const startDate = moment("2020-08-01").toDate();

  const [hoverValue, setHoverValue] = useState<HoverValue>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (event: MouseEvent) => {
      setMousePos({ x: event.clientX, y: event.clientY });
      console.log("Mouse Position:", mousePos); // Debugging log
    };

    window.addEventListener("mousemove", handleMouseMove);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, [mousePos]);

  useEffect(() => {
    // Ensure bootstrap is available globally
    const bootstrap = (window as any).bootstrap;
    if (bootstrap) {
      const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-toggle="tooltip"]')
      );
      const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
      });

      // Clean up tooltips on unmount
      return () => {
        tooltipList.forEach((tooltip) => tooltip.dispose());
      };
    } else {
      console.error("Bootstrap is not available");
    }
  }, [hoverValue]);

  return (
    <div className="heatmap-container" style={{ position: "relative" }}>
      <CalendarHeatmap
        startDate={startDate}
        endDate={moment().subtract(4, "year").toDate()}
        values={heatmapData}
        classForValue={(value) => {
          console.log("Value:", value); // Debugging log
          if (!value) {
            return "color-empty";
          }
          return `color-github-${Math.min(4, Math.ceil(value.count / 2))}`;
        }}
        showOutOfRangeDays
        showWeekdayLabels
        onMouseOver={(_event, value) => {
          console.log("Mouse Over Value:", value); // Debugging log
          setHoverValue(value || null);
        }}
        onMouseLeave={() => {
          console.log("Mouse Leave"); // Debugging log
          setHoverValue(null);
        }}
      />
      {hoverValue && (
        <div
          className="tooltip"
          style={{ top: mousePos.y + 10, left: mousePos.x + 10 }}
          data-toggle="tooltip"
          title={`${hoverValue.date}: ${hoverValue.count}`}
        >
          {/* Placeholder element for the tooltip */}
        </div>
      )}
    </div>
  );
};

export default CommitHeatmap;
