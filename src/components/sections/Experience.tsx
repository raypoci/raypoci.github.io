import React from 'react';
import { motion } from 'framer-motion';
import { FaCalendar, FaMapMarker } from 'react-icons/fa';
import { portfolioData } from '../../data/portfolioData';

export const Experience: React.FC = () => {
  return (
    <section id="experience" className="py-20 bg-white dark:bg-gray-900">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-12 text-center">
            Experience
          </h2>

          <div className="max-w-4xl mx-auto">
            {portfolioData.experiences.map((exp, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="mb-12"
              >
                <div className="bg-gray-50 dark:bg-gray-800 rounded-xl p-6 border border-gray-100 dark:border-gray-700">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                        {exp.position}
                      </h3>
                      <p className="text-lg text-primary mt-1">{exp.company}</p>
                    </div>
                    <div className="flex items-center space-x-4 mt-4 md:mt-0 text-sm text-gray-500 dark:text-gray-400">
                      <div className="flex items-center">
                        <FaCalendar className="w-4 h-4 mr-1" />
                        {exp.date}
                      </div>
                      <div className="flex items-center">
                        <FaMapMarker className="w-4 h-4 mr-1" />
                        {exp.location}
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {exp.responsibilities.map((resp, idx) => (
                      <p key={idx} className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
                        {resp}
                      </p>
                    ))}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
};
