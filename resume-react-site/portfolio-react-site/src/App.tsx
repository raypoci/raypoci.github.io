import { useState } from "react";
import { Navbar, NavbarProps } from "./components/Navbar"; // Adjust the path as needed
import "./App.css"; // Optional: Include any global styles
import { About } from "./components/About";
import Experience from "./components/Experience";

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

const responsibilities = [
  "Onboarded and mentored 6 new team members, ensuring seamless integration by providing active training and guidance, fostering technical expertise.",
  "Effectively managed team members' work, promoting productivity.",
  "Contributed to interviewing and hiring top talent software developers.",
  "Helped shape team composition, driving growth and innovation.",
  "Contributed to the development of scalable Java 11 applications using Spring Boot and Azure Functions within Data Quality Micro Service.",
  "Implemented comprehensive exception management framework, ensuring robust error handling across all Data Quality Applications.",
  "Built a Java 11 based Spring-boot application from scratch to schedule Data Quality events. Successfully addressed business needs through automated event management.",
  "Authored thousands of lines of reusable Python code to streamline day-to-day operations, including Data Quality Control configuration, Workflow integration, and Automated Git code pushes.",
  "Developed and configured hundreds of parameterizable SQL controls for data validation in Snowflake, Oracle, and SQLServer databases. Ensured data accuracy, completeness, uniqueness, and other custom checks across 8 distinct data products and 12+ clients.",
  "Implemented flexible, client-agnostic, and context-independent design.",
  "Designed and implemented a tolerance table system to enhance Data Quality controls. Enabled flexible data validation thresholds.",
  "Used CI/CD principles in development through GitHub, RTC Docker image builds, as well as Azure Kubernetes deployment via ADO pipelines.",
  "Utilized Agile methodology for iterative and incremental development. Collaborated with cross-functional teams for Sprint planning, Daily stand-ups, Retrospectives, and Continuous improvement.",
];

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
            <Experience
              position="Software Engineer (AVP / Data Quality)"
              company="State Street Corporation"
              date="09/2021 - Present"
              location="Boston, MA"
              responsibilities={responsibilities}
            />
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
