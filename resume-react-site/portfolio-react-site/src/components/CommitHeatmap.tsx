import React, { useEffect, useState, useRef } from "react";
import CalendarHeatmap from "react-calendar-heatmap";
import "react-calendar-heatmap/dist/styles.css";
import moment from "moment";
import { Tooltip } from "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "../App.css";
import { fetchCommits, Commit, RepoConfig } from "../utils/FetchCommits";

interface HeatmapValue {
  date: string;
  count: number;
}

interface ReactCalendarHeatmapValue<T> {
  date: T;
  count?: number;
}

const CommitHeatmap: React.FC = () => {
  const [commits, setCommits] = useState<Commit[]>([]);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const currentTooltip = useRef<Tooltip | null>(null);
  const heatmapRef = useRef<HTMLDivElement>(null);

  const [repos] = useState<RepoConfig[]>([
    {
      owner: "raypoci",
      name: "ReiLovesDiana",
      isPrivate: true,
    },
    {
      owner: "raypoci",
      name: "betting_AI",
      isPrivate: true,
    },
    {
      owner: "raypoci",
      name: "raypoci.github.io",
      isPrivate: false,
    },
  ]);

  // You should store this securely, preferably in environment variables
  const GITHUB_TOKEN = import.meta.env.VITE_GITHUB_API_TOKEN;

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchCommits(repos, GITHUB_TOKEN);
      setCommits(data);
    };
    fetchData();
  }, [repos]);

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
  const heatmapData: HeatmapValue[] = Object.keys(groupedCommits).map(
    (date) => ({
      date: date,
      count: groupedCommits[date],
    })
  );

  const startDate = moment("2020-08-01").toDate();

  const handleMouseOver = (
    event: React.MouseEvent<SVGRectElement>,
    value: ReactCalendarHeatmapValue<string> | undefined
  ) => {
    if (value && tooltipRef.current && event.currentTarget) {
      // Get the cell's position
      const rect = event.currentTarget.getBoundingClientRect();
      const heatmapRect = heatmapRef.current?.getBoundingClientRect();

      if (heatmapRect) {
        // Calculate position relative to heatmap container
        const offsetX = rect.left - heatmapRect.left;
        const offsetY = rect.top - heatmapRect.top;

        // Position tooltip
        tooltipRef.current.style.left = `${offsetX + rect.width / 2}px`;
        tooltipRef.current.style.top = `${offsetY - 5}px`;
        tooltipRef.current.style.transform = "translate(-50%, -100%)";

        // Dispose of any existing tooltip
        if (currentTooltip.current) {
          currentTooltip.current.dispose();
        }

        const formattedDate = moment(value.date).format("MMM D, YYYY");
        tooltipRef.current.setAttribute(
          "data-bs-title",
          `${value.count} commit${
            value.count !== 1 ? "s" : ""
          } on ${formattedDate}`
        );

        // Create new tooltip
        currentTooltip.current = new Tooltip(tooltipRef.current, {
          placement: "top",
          trigger: "manual",
          container: "body",
        });

        // Show the tooltip
        currentTooltip.current.show();
      }
    }
  };

  const handleMouseLeave = () => {
    if (currentTooltip.current) {
      currentTooltip.current.hide();
      currentTooltip.current.dispose();
      currentTooltip.current = null;
    }
  };

  return (
    <div className="heatmap-container" ref={heatmapRef}>
      <div
        ref={tooltipRef}
        className="custom-tooltip"
        data-bs-toggle="tooltip"
      />
      <CalendarHeatmap
        startDate={startDate}
        endDate={moment().subtract(4, "years").toDate()}
        values={heatmapData}
        classForValue={(value) => {
          if (!value) {
            return "color-empty";
          }
          return `color-github-${Math.min(4, Math.ceil(value.count / 2))}`;
        }}
        showOutOfRangeDays
        onMouseOver={handleMouseOver}
        onMouseLeave={handleMouseLeave}
      />
    </div>
  );
};

export default CommitHeatmap;
