import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGithub, faLinkedin } from "@fortawesome/free-brands-svg-icons";
import { faEnvelope } from "@fortawesome/free-solid-svg-icons";
import CommitHeatmap from "./CommitHeatmap";
import "../App.css"; // Ensure the path is correct

interface AboutProps {
  githubUser: string;
  linkedinUser: string;
  email: string;
  imageSrc: string;
}

export const About = ({
  githubUser,
  linkedinUser,
  email,
  imageSrc,
}: AboutProps) => {
  return (
    <div className="about-container container">
      <div className="row">
        <div className="col-md-6 d-flex flex-column align-items-center">
          <img
            src={"src/assets/" + imageSrc} // Adjust the path as needed
            alt="Profile"
            className="profile-image img-fluid responsive-logo" // Add responsive-logo class
          />
          <p className="job-position">Senior Software Developer</p>
          <div className="icon-bar">
            <a
              href={"https://github.com/" + githubUser}
              target="_blank"
              rel="noopener noreferrer"
            >
              <FontAwesomeIcon icon={faGithub} size="2x" />
            </a>
            <a
              href={"https://www.linkedin.com/in/" + linkedinUser}
              target="_blank"
              rel="noopener noreferrer"
            >
              <FontAwesomeIcon icon={faLinkedin} size="2x" />
            </a>
            <a href={"mailto:" + email}>
              <FontAwesomeIcon icon={faEnvelope} size="2x" />
            </a>
          </div>
        </div>
        <div className="col-md-6 d-flex flex-column justify-content-center">
          <p className="welcome"> Welcome {"\u{1F44B}"}, I'm Rei.</p>
          <p className="introduction text-content">
            Highly accomplished software engineer at State Street's Data Quality
            Team (3+ yrs). Expertise in SQL, Java, Python, Agile, Mentorship &
            Automation. Delivers scalable solutions, drives innovation and
            collaborates cross-functionally. Proven track record in application
            development, junior engineer mentorship & process optimization.
          </p>
        </div>
      </div>
      <div className="container github-activity">
        <h2 className="github-activity-text">Github Activity</h2>
        <CommitHeatmap />
      </div>
    </div>
  );
};
