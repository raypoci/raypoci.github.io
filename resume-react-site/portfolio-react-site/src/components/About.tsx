import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGithub, faLinkedin } from "@fortawesome/free-brands-svg-icons";
import { faEnvelope } from "@fortawesome/free-solid-svg-icons";
import CommitHeatmap from "./CommitHeatmap";

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
    <>
      <div className="container">
        <div className="row">
          <div className="col-md-6">
            <p className="welcome"> Welcome {"\u{1F44B}"}, I'm</p>
            <img
              src={"src/assets/" + imageSrc} // Adjust the path as needed
              alt="Site Logo"
              height="auto"
              className="img-fluid about-photo"
            ></img>
            <h1 className="owner-name">Rei</h1>
            <p className="job-position">Software Developer</p>
            <div className="icon-bar">
              {" "}
              <a
                href={"https://github.com/" + githubUser}
                target="_blank"
                rel="noopener noreferrer"
              >
                {" "}
                <FontAwesomeIcon icon={faGithub} size="2x" />{" "}
              </a>{" "}
              <a
                href={"https://www.linkedin.com/in/" + linkedinUser}
                target="_blank"
                rel="noopener noreferrer"
              >
                {" "}
                <FontAwesomeIcon icon={faLinkedin} size="2x" />{" "}
              </a>{" "}
              <a href={"mailto:" + email}>
                {" "}
                <FontAwesomeIcon icon={faEnvelope} size="2x" />{" "}
              </a>{" "}
            </div>
          </div>
          <div className="col-md-6">
            <p className="introduction">
              Highly accomplished software engineer at State Street's Data
              Quality Team (3+ yrs). Expertise in SQL, Java, Python, Agile,
              Mentorship & Automation. Delivers scalable solutions, drives
              innovation and collaborates cross-functionally. Proven track
              record in application development, junior engineer mentorship &
              process optimization.
            </p>
            <CommitHeatmap />
          </div>
        </div>
      </div>
    </>
  );
};
