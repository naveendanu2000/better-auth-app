import type { ReactElement } from "react";
import { VscLoading } from "react-icons/vsc";

const Button = ({
  loading,
  loadingText,
  disabled,
  name,
  icon,
  onClick,
  type,
}: {
  loading?: boolean;
  disabled?: boolean;
  loadingText?: string;
  icon?: ReactElement;
  onClick?: () => void;
  name: string;
  type?: "submit" | "reset" | "button" | undefined;
}) => {
  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      className="items-center font-semibold rounded text-black flex gap-2 px-4 py-2 shadow hover:shadow-xl active:shadow-lg cursor-pointer bg-white/50 backdrop-blur-3xl disabled:opacity-65 disabled:hover:shadow disabled:cursor-not-allowed hover:backdrop-blur-lg hover:bg-white/20"
    >
      {loading ? (
        <>
          <VscLoading className="animate-spin text-2xl" /> {loadingText}{" "}
        </>
      ) : (
        <>
          {icon}
          {name}
        </>
      )}
    </button>
  );
};

export default Button;
