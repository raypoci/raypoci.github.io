interface Props {
  color?: "primary" | "secondary" | "danger" | "success";
  children: string;
  onClick: () => void;
}

export const AlertButtons = ({
  color = "primary",
  children,
  onClick,
}: Props) => {
  return (
    <button className={"btn btn-" + color} onClick={onClick}>
      {children}
    </button>
  );
};
