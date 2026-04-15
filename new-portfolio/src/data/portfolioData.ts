export interface Experience {
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

export interface Skill {
  name: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced' | 'Expert';
  category: 'Languages' | 'Frameworks' | 'Tools' | 'Cloud' | 'Databases' | 'Other';
}

export interface Project {
  title: string;
  description: string;
  technologies: string[];
  github?: string;
  live?: string;
  image?: string;
}

export interface Education {
  institution: string;
  degree: string;
  date: string;
  location: string;
}

export interface Contact {
  email: string;
  github: string;
  linkedin: string;
}

export const portfolioData = {
  personalInfo: {
    name: 'Rei',
    title: 'Senior Software Developer',
    tagline: 'Building scalable solutions with expertise in Java, Python, SQL, and cloud technologies.',
    about: 'Highly accomplished software engineer at State Street\'s Data Quality Team (3+ years). Expertise in SQL, Java, Python, Agile, Mentorship & Automation. Delivers scalable solutions, drives innovation and collaborates cross-functionally. Proven track record in application development, junior engineer mentorship & process optimization.',
    email: 'raypoci18@gmail.com',
    github: 'https://github.com/raypoci',
    linkedin: 'https://www.linkedin.com/in/ray-poci',
  },
  experiences: [
    {
      position: 'Vice President, Senior Software Developer',
      company: 'State Street Corporation',
      date: '12/2024 - Present',
      location: 'Boston, MA',
      responsibilities: [
        'Onboarded and mentored 6 new team members, ensuring seamless integration by providing active training and guidance, fostering technical expertise.',
        'Effectively managed team members\' work, promoting productivity.',
        'Contributed to interviewing and hiring top talent software developers.',
        'Helped shape team composition, driving growth and innovation.',
        'Contributed to the development of scalable Java 11 applications using Spring Boot and Azure Functions within Data Quality Micro Service.',
        'Implemented comprehensive exception management framework, ensuring robust error handling across all Data Quality Applications.',
        'Built a Java 11 based Spring-boot application from scratch to schedule Data Quality events. Successfully addressed business needs through automated event management.',
        'Authored thousands of lines of reusable Python code to streamline day-to-day operations, including Data Quality Control configuration, Workflow integration, and Automated Git code pushes.',
        'Developed and configured hundreds of parameterizable SQL controls for data validation in Snowflake, Oracle, and SQLServer databases. Ensured data accuracy, completeness, uniqueness, and other custom checks across 8 distinct data products and 12+ clients.',
        'Implemented flexible, client-agnostic, and context-independent design.',
        'Designed and implemented a tolerance table system to enhance Data Quality controls. Enabled flexible data validation thresholds.',
        'Used CI/CD principles in development through GitHub, RTC Docker image builds, as well as Azure Kubernetes deployment via ADO pipelines.',
        'Utilized Agile methodology for iterative and incremental development. Collaborated with cross-functional teams for Sprint planning, Daily stand-ups, Retrospectives, and Continuous improvement.',
      ],
      image: {
        src: '/images/state-street-logo.svg',
        alt: 'State Street Corporation',
      },
    },
    {
      position: 'Assistant Vice President, Software Developer',
      company: 'State Street Corporation',
      date: '05/2023 - 12/2024',
      location: 'Boston, MA',
      responsibilities: [
        'Led cross-functional teams in developing innovative software solutions, driving strategic initiatives, and improving operational efficiencies.',
        'Effectively managed team members\' work, promoting productivity.',
        'Contributed to interviewing and hiring top talent software developers.',
        'Helped shape team composition, driving growth and innovation.',
        'Contributed to the development of scalable Java 11 applications using Spring Boot and Azure Functions within Data Quality Micro Service.',
        'Implemented comprehensive exception management framework, ensuring robust error handling across all Data Quality Applications.',
        'Built a Java 11 based Spring-boot application from scratch to schedule Data Quality events. Successfully addressed business needs through automated event management.',
        'Authored thousands of lines of reusable Python code to streamline day-to-day operations, including Data Quality Control configuration, Workflow integration, and Automated Git code pushes.',
        'Developed and configured hundreds of parameterizable SQL controls for data validation in Snowflake, Oracle, and SQLServer databases. Ensured data accuracy, completeness, uniqueness, and other custom checks across 8 distinct data products and 12+ clients.',
        'Implemented flexible, client-agnostic, and context-independent design.',
        'Designed and implemented a tolerance table system to enhance Data Quality controls. Enabled flexible data validation thresholds.',
        'Used CI/CD principles in development through GitHub, RTC Docker image builds, as well as Azure Kubernetes deployment via ADO pipelines.',
        'Utilized Agile methodology for iterative and incremental development. Collaborated with cross-functional teams for Sprint planning, Daily stand-ups, Retrospectives, and Continuous improvement.',
      ],
      image: {
        src: '/images/state-street-logo.svg',
        alt: 'State Street Corporation',
      },
    },
    {
      position: 'Officer, Junior Software Developer',
      company: 'State Street Corporation',
      date: '09/2021 - 05/2023',
      location: 'Boston, MA',
      responsibilities: [
        'Managed end-to-end software development lifecycle, ensuring timely delivery and adherence to industry standards.',
        'Effectively managed team members\' work, promoting productivity.',
        'Contributed to interviewing and hiring top talent software developers.',
        'Helped shape team composition, driving growth and innovation.',
        'Contributed to the development of scalable Java 11 applications using Spring Boot and Azure Functions within Data Quality Micro Service.',
        'Implemented comprehensive exception management framework, ensuring robust error handling across all Data Quality Applications.',
        'Built a Java 11 based Spring-boot application from scratch to schedule Data Quality events. Successfully addressed business needs through automated event management.',
        'Authored thousands of lines of reusable Python code to streamline day-to-day operations, including Data Quality Control configuration, Workflow integration, and Automated Git code pushes.',
        'Developed and configured hundreds of parameterizable SQL controls for data validation in Snowflake, Oracle, and SQLServer databases. Ensured data accuracy, completeness, uniqueness, and other custom checks across 8 distinct data products and 12+ clients.',
        'Implemented flexible, client-agnostic, and context-independent design.',
        'Designed and implemented a tolerance table system to enhance Data Quality controls. Enabled flexible data validation thresholds.',
        'Used CI/CD principles in development through GitHub, RTC Docker image builds, as well as Azure Kubernetes deployment via ADO pipelines.',
        'Utilized Agile methodology for iterative and incremental development. Collaborated with cross-functional teams for Sprint planning, Daily stand-ups, Retrospectives, and Continuous improvement.',
      ],
      image: {
        src: '/images/state-street-logo.svg',
        alt: 'State Street Corporation',
      },
    },
  ] as Experience[],
  skills: [
    { name: 'Java', level: 'Expert', category: 'Languages' },
    { name: 'Python', level: 'Expert', category: 'Languages' },
    { name: 'SQL', level: 'Expert', category: 'Databases' },
    { name: 'Spring Boot', level: 'Expert', category: 'Frameworks' },
    { name: 'Azure Functions', level: 'Advanced', category: 'Cloud' },
    { name: 'Docker', level: 'Advanced', category: 'Tools' },
    { name: 'Kubernetes', level: 'Advanced', category: 'Cloud' },
    { name: 'GitHub Actions', level: 'Advanced', category: 'Tools' },
    { name: 'Snowflake', level: 'Advanced', category: 'Databases' },
    { name: 'Oracle', level: 'Advanced', category: 'Databases' },
    { name: 'SQL Server', level: 'Advanced', category: 'Databases' },
    { name: 'Agile/Scrum', level: 'Expert', category: 'Other' },
    { name: 'Mentorship', level: 'Expert', category: 'Other' },
    { name: 'Automation', level: 'Expert', category: 'Other' },
  ] as Skill[],
  projects: [
    {
      title: 'Data Quality Micro Service',
      description: 'Scalable Java 11 application built with Spring Boot and Azure Functions for comprehensive data quality validation across multiple clients.',
      technologies: ['Java', 'Spring Boot', 'Azure Functions', 'Docker', 'Kubernetes'],
      github: 'https://github.com/raypoci/data-quality-service',
    },
    {
      title: 'Automated Event Scheduler',
      description: 'Custom-built Java application for scheduling and managing Data Quality events with automated workflows.',
      technologies: ['Java', 'Spring Boot', 'Python', 'CI/CD'],
      github: 'https://github.com/raypoci/event-scheduler',
    },
    {
      title: 'Data Validation Framework',
      description: 'Parameterizable SQL controls for data validation across Snowflake, Oracle, and SQL Server databases.',
      technologies: ['SQL', 'Snowflake', 'Oracle', 'SQL Server'],
      github: 'https://github.com/raypoci/validation-framework',
    },
  ] as Project[],
  education: [
    {
      institution: 'State Street Corporation',
      degree: 'Professional Development',
      date: '2021 - Present',
      location: 'Boston, MA',
    },
  ] as Education[],
  contact: {
    email: 'raypoci18@gmail.com',
    github: 'https://github.com/raypoci',
    linkedin: 'https://www.linkedin.com/in/ray-poci',
  } as Contact,
  navbar: [
    { name: 'About', link: '#about' },
    { name: 'Experience', link: '#experience' },
    { name: 'Skills', link: '#skills' },
    { name: 'Projects', link: '#projects' },
    { name: 'Education', link: '#education' },
    { name: 'Contact', link: '#contact' },
  ],
};
