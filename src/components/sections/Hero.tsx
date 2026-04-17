import React from "react";
import { motion } from "framer-motion";
import { FaEnvelope, FaGithub, FaLinkedin } from "react-icons/fa";
import { portfolioData } from "../../data/portfolioData";

export const Hero: React.FC = () => {
  return (
    <section
      id="about"
      className="min-h-screen flex items-center justify-center pt-16 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800"
    >
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 dark:text-white mb-6">
              <span className="text-primary">
                {portfolioData.personalInfo.name}
              </span>
            </h1>
            <h2 className="text-2xl md:text-4xl text-gray-600 dark:text-gray-300 mb-4">
              {portfolioData.personalInfo.title}
            </h2>
            <p className="text-xl text-gray-500 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
              {portfolioData.personalInfo.tagline}
            </p>
            <p className="text-lg text-gray-600 dark:text-gray-400 mb-12 max-w-3xl mx-auto leading-relaxed">
              {portfolioData.personalInfo.about}
            </p>

            <div className="flex flex-wrap justify-center gap-4 mb-12">
              <a
                href={`mailto:${portfolioData.personalInfo.email}`}
                className="inline-flex items-center px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors duration-200 font-medium"
              >
                <FaEnvelope className="w-5 h-5 mr-2" />
                Contact Me
              </a>
              <a
                href={portfolioData.contact.github}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-6 py-3 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200 font-medium border border-gray-200 dark:border-gray-700"
              >
                <FaGithub className="w-5 h-5 mr-2" />
                GitHub
              </a>
              <a
                href={portfolioData.contact.linkedin}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-6 py-3 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200 font-medium border border-gray-200 dark:border-gray-700"
              >
                <FaLinkedin className="w-5 h-5 mr-2" />
                LinkedIn
              </a>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};
