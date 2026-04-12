import React from "react";
import FloatingBullets from "../utils/FloatingBullets";

export interface ExperienceProps {
  position: string;
  company: string;
  date: string;
  location: string;
  responsibilities: string[];
  image: {
    src: string;
    alt: string;
  };
}

//"src/assets/State-street-logo-final.svg"

const Experience: React.FC<ExperienceProps> = ({
  position,
  company,
  date,
  location,
  responsibilities,
  image,
}) => {
  return (
    <div className="experience-card">
      <div className="experience-header">
        <img src={image.src} alt={image.alt} className="company-logo" />
        <div>
          <h2>{position}</h2>
          <h3>{company}</h3>
          <p>{date}</p>
          <p>{location}</p>
        </div>
      </div>
      <FloatingBullets bulletPoints={responsibilities} />
    </div>
  );
};

export default Experience;
