import React from "react";
import { motion } from "framer-motion";
import { FaEnvelope, FaGithub, FaLinkedin } from "react-icons/fa";
import { portfolioData } from "../../data/portfolioData";

export const Contact: React.FC = () => {
  return (
    <section id="contact" className="py-20 bg-white dark:bg-gray-900">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-12 text-center">
            Get In Touch
          </h2>

          <div className="max-w-4xl mx-auto bg-gray-50 dark:bg-gray-800 rounded-xl p-8 border border-gray-100 dark:border-gray-700">
            <div className="text-center mb-8">
              <p className="text-xl text-gray-600 dark:text-gray-300 mb-6">
                Interested in working together or have a question? Feel free to
                reach out!
              </p>
              <a
                href={`mailto:${portfolioData.contact.email}`}
                className="inline-flex items-center px-8 py-4 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors duration-200 font-medium text-lg"
              >
                <FaEnvelope className="w-5 h-5 mr-2" />
                Send Me an Email
              </a>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="flex flex-col items-center p-6 bg-white dark:bg-gray-700 rounded-lg border border-gray-100 dark:border-gray-600"
              >
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                  <FaEnvelope className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Email
                </h3>
                <a
                  href={`mailto:${portfolioData.contact.email}`}
                  className="text-primary hover:underline"
                >
                  {portfolioData.contact.email}
                </a>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.05 }}
                className="flex flex-col items-center p-6 bg-white dark:bg-gray-700 rounded-lg border border-gray-100 dark:border-gray-600"
              >
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                  <FaGithub className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  GitHub
                </h3>
                <a
                  href={portfolioData.contact.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary hover:underline"
                >
                  {portfolioData.contact.github}
                </a>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.05 }}
                className="flex flex-col items-center p-6 bg-white dark:bg-gray-700 rounded-lg border border-gray-100 dark:border-gray-600"
              >
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                  <FaLinkedin className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  LinkedIn
                </h3>
                <a
                  href={portfolioData.contact.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary hover:underline"
                >
                  {portfolioData.contact.linkedin}
                </a>
              </motion.div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};
