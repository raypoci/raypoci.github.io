export function generateUniqueKey(): string {
  const timestamp = Date.now(); // Current timestamp in milliseconds
  const randomValue = Math.random(); // Random number between 0 and 1
  const calc = timestamp - randomValue;
  console.log(calc);
  return `${calc}`;
}

// Example usage
const uniqueKey = generateUniqueKey();
console.log(uniqueKey);
