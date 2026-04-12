import { useState } from "react";
import { Navbar } from "./components/Navbar"; // Adjust the path as needed
import "./App.css"; // Optional: Include any global styles
import { About } from "./components/About";
import Experience from "./components/Experience";
import NavbarData from "./data/NavbarData";
import { ExperienceData } from "./data/ExperienceData";

const nav_object = NavbarData;
const experience_object = ExperienceData;


function App() {
  const [activeSection, setActiveSection] = useState("about");
  const githubUserName = "raypoci";
  const linkedinUserName = "ray-poci";
  const email = "raypoci18@gmail.com";
  const aboutPhoto = "selfie2.jpg";

  return (
    <div className="App">
      <Navbar items={nav_object} setActiveSection={setActiveSection} />
      <div className="content">
        {activeSection === "about" && (
          <section id="about">
            <About
              githubUser={githubUserName}
              linkedinUser={linkedinUserName}
              email={email}
              imageSrc={aboutPhoto}
            />
          </section>
        )}
        {activeSection === "experience" && (
          <section id="experience">
            {experience_object.map((item) => (
              <Experience
                position={item.position}
                company={item.company}
                date={item.date}
                location={item.location}
                responsibilities={item.responsibilities}
                image={item.image}
              />
            ))}
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
