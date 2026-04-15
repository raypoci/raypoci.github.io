import React from 'react';
import { motion } from 'framer-motion';
import { portfolioData } from '../../data/portfolioData';

const skillIcons: Record<string, string> = {
  Languages: '💻',
  Frameworks: '🔧',
  Tools: '🛠️',
  Cloud: '☁️',
  Databases: '🗄️',
  Other: '✨',
};

export const Skills: React.FC = () => {
  const groupedSkills = portfolioData.skills.reduce((acc, skill) => {
    if (!acc[skill.category]) {
      acc[skill.category] = [];
    }
    acc[skill.category].push(skill);
    return acc;
  }, {} as Record<string, typeof portfolioData.skills>);

  return (
    <section id="skills" className="py-20 bg-gray-50 dark:bg-gray-800">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-12 text-center">
            Skills & Technologies
          </h2>

          <div className="max-w-4xl mx-auto">
            {Object.entries(groupedSkills).map(([category, skills]) => (
              <motion.div
                key={category}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: Number(category) * 0.1 }}
                viewport={{ once: true }}
                className="mb-8"
              >
                <h3 className="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center">
                  <span className="text-2xl mr-2">{skillIcons[category]}</span>
                  {category}
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                  {skills.map((skill, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, scale: 0.9 }}
                      whileInView={{ opacity: 1, scale: 1 }}
                      transition={{ duration: 0.3, delay: idx * 0.05 }}
                      viewport={{ once: true }}
                      className={`p-4 rounded-lg border ${
                        skill.level === 'Expert'
                          ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
                          : skill.level === 'Advanced'
                          ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800'
                          : skill.level === 'Intermediate'
                          ? 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800'
                          : 'bg-gray-50 dark:bg-gray-700 border-gray-200 dark:border-gray-600'
                      }`}
                    >
                      <span className="font-medium text-gray-900 dark:text-white">{skill.name}</span>
                      <span className="text-sm text-gray-500 dark:text-gray-400 ml-2">
                        ({skill.level})
                      </span>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
};
