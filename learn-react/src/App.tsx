import { useState } from "react";
import Alert from "./components/Alert";
import { AlertButtons } from "./components/AlertButtons";

function App() {
  const [displayVisibility, setDisplayVisibility] = useState(true);

  const handleVisibility = () => {
    displayVisibility
      ? setDisplayVisibility(false)
      : setDisplayVisibility(true);
  };

  const buttonDiv = (
    <AlertButtons onClick={handleVisibility}>My Button</AlertButtons>
  );

  const alertDiv = <Alert onClose={handleVisibility}>This is an alert</Alert>;

  return <div>{displayVisibility ? buttonDiv : alertDiv}</div>;
}

export default App;
