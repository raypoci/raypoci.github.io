import React, { useState } from "react";
import { capitalizeFirstLetter } from "../utils/JSFunctions";

export interface NavbarProps {
  name: string;
  link: string;
}

interface NavbarComponentProps {
  items: NavbarProps[];
  setActiveSection: (section: string) => void;
}

export const Navbar: React.FC<NavbarComponentProps> = ({
  items,
  setActiveSection,
}) => {
  const [activeItem, setActiveItem] = useState("about");
  const [isToggled, setIsToggled] = useState(false); // State to track toggle

  const handleItemClick = (item: string) => {
    setActiveItem(item);
    setActiveSection(item);
    setIsToggled(false); // Hide menu after selection
  };

  const handleLogoClick = () => {
    setActiveItem("about");
    setActiveSection("about");
    setIsToggled(false); // Hide menu after selection
  };

  const handleToggle = () => {
    setIsToggled(!isToggled);
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark flex-column vh-100 position-fixed wider-navbar">
      {!isToggled && (
        <button
          className="navbar-toggler"
          type="button"
          aria-controls="navbarSupportedContent"
          aria-expanded={isToggled ? "true" : "false"}
          aria-label="Toggle navigation"
          onClick={handleToggle}
        >
          <span className="navbar-toggler-icon"></span>
        </button>
      )}

      <div
        className={`collapse navbar-collapse flex-column align-items-center justify-content-center ${
          isToggled ? "show" : ""
        }`}
        id="navbarSupportedContent"
      >
        <ul className="navbar-nav flex-column w-100 align-items-center">
          {!isToggled && (
            <li className="nav-item mb-4">
              <a
                className="navbar-brand d-flex align-items-center justify-content-center"
                href="#about"
                onClick={handleLogoClick}
              >
                <img
                  src="src/assets/selfie2.jpg" // Adjust the path as needed
                  alt="Site Logo"
                  height="auto"
                  className="img-fluid responsive-logo"
                />
              </a>
            </li>
          )}
          {items.map((item) => (
            <li
              key={item.name}
              className={`nav-item ${
                activeItem === item.name ? "custom-active" : ""
              }`}
            >
              <a
                className="nav-link"
                href={item.link}
                onClick={() => handleItemClick(item.name)}
              >
                {capitalizeFirstLetter(item.name)}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
};
