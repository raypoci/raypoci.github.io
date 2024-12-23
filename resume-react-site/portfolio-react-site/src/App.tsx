import { useState } from "react";
import { Navbar, NavbarProps } from "./components/Navbar"; // Adjust the path as needed
import "./App.css"; // Optional: Include any global styles

const nav_object: NavbarProps[] = [
  {
    name: "about",
    link: "#about", // Update link to match the id of the section
  },
  {
    name: "experience",
    link: "#experience", // Update link to match the id of the section
  },
  {
    name: "education",
    link: "#education", // Update link to match the id of the section
  },
  {
    name: "skills",
    link: "#skills", // Update link to match the id of the section
  },
  {
    name: "interests",
    link: "#interests", // Update link to match the id of the section
  },
];

function App() {
  const [activeSection, setActiveSection] = useState("about");

  return (
    <div className="App">
      <Navbar items={nav_object} setActiveSection={setActiveSection} />
      <div className="content">
        {activeSection === "about" && (
          <section id="about">
            <h1>About Me</h1>
            <p>This is the About section.</p>
          </section>
        )}
        {activeSection === "experience" && (
          <section id="experience">
            <h1>Experience</h1>
            <p>This is the Experience section.</p>
          </section>
        )}
        {activeSection === "education" && (
          <section id="education">
            <h1>Education</h1>
            <p>This is the Education section.</p>
          </section>
        )}
        {activeSection === "skills" && (
          <section id="skills">
            <h1>Skills</h1>
            <p>This is the Skills section.</p>
          </section>
        )}
        {activeSection === "interests" && (
          <section id="interests">
            <h1>Interests</h1>
            <p>This is the Interests section.</p>
          </section>
        )}
      </div>
    </div>
  );
}

export default App;
