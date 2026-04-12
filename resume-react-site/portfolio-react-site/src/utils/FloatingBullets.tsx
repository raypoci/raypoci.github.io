import React, { useEffect } from "react";
import { generateUniqueKey } from "./GenerateUniqueKey";

interface BulletProps {
  text: string;
}

interface BulletListProps {
  bulletPoints: string[];
}

const Bullet: React.FC<BulletProps> = ({ text }) => {
  return <div className="bullet">{text}</div>;
};

const FloatingBullets: React.FC<BulletListProps> = ({ bulletPoints }) => {
  useEffect(() => {
    const bullets = document.querySelectorAll(".bullet");
    bullets.forEach((bullet, index) => {
      const interval = setInterval(() => {
        (
          bullet as HTMLElement
        ).style.animation = `floatIn 1s ease-out forwards`;
      }, index * 10); // Adjust the delay as needed
      return () => clearInterval(interval); // Cleanup the interval on component unmount
    });
  }, []);

  return (
    <div className="floating-bullets">
      {bulletPoints.map((bulletItem) => (
        <Bullet key={generateUniqueKey()} text={bulletItem} />
      ))}
    </div>
  );
};

export default FloatingBullets;
