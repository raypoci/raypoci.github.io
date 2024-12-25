import React from "react";

interface ExperienceProps {
  position: string;
  company: string;
  date: string;
  location: string;
  responsibilities: string[];
}

const Experience: React.FC<ExperienceProps> = ({
  position,
  company,
  date,
  location,
  responsibilities,
}) => {
  return (
    <div className="experience-container">
      <h2>WORK EXPERIENCE</h2>
      <div className="experience-details">
        <h3>{position}</h3>
        <h4>{company}</h4>
        <p>{date}</p>
        <p>{location}</p>
      </div>
      <ul className="responsibilities-list">
        {responsibilities.map((responsibility, index) => (
          <li key={index}>{responsibility}</li>
        ))}
      </ul>
    </div>
  );
};

export default Experience;
