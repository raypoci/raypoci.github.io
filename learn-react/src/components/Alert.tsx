import { ReactNode } from "react";

interface Props {
  children: ReactNode;
  color?: "primary" | "secondary" | "danger" | "success";
  onClose: () => void;
}

const Alert = ({ children, onClose, color = "primary" }: Props) => {
  return (
    <div className={"alert alert-dismissible alert-" + color}>
      <>
        <p>{children}</p>
        <button
          className="btn-close position-absolute end-0 top-0"
          data-bs-dismiss="alert"
          aria-label="Close"
          onClick={onClose}
        ></button>
      </>
    </div>
  );
};

export default Alert;
