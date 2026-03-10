const Input = ({
  id,
  name,
  placeholder,
  className,
  type = "text",
  defaultValue,
}: {
  id?: string;
  name?: string;
  placeholder?: string;
  className?: string;
  type?: string;
  defaultValue?: string;
}) => {
  return (
    <input
      autoComplete="off"
      id={id}
      name={name}
      type={type}
      defaultValue={defaultValue}
      className={`rounded m-auto px-4 min-w-70 text-center py-3 hover:shadow-xl shadow focus:shadow-lg focus:outline-none bg-white/50 ${className}`}
      placeholder={placeholder}
    />
  );
};

export default Input;
