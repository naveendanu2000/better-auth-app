import { useActionState, useEffect, useState } from "react";
import Input from "../components/small-components/Input";
import { getUserDetails, login } from "../api/auth-api";
import toast from "react-hot-toast";
import { VscLoading } from "react-icons/vsc";
import { useNavigate } from "react-router-dom";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { FaGoogle } from "react-icons/fa";

interface InitialState {
  success: boolean;
  error: { username: string; password: string };
  values: { username: string; password: string };
}

const initialState: InitialState = {
  success: false,
  error: { username: "", password: "" },
  values: { username: "", password: "" },
};

const LoginPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const getCurrentUser = async () => {
      setLoading(true);
      try {
        const response = await getUserDetails();

        if (response) {
          toast.success("Already logged in");
          navigate("/user");
        }
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    };

    getCurrentUser();

    return () => setLoading(false);
  }, [navigate]);

  const actionState = async (
    prevState: InitialState,
    formData: FormData,
  ): Promise<InitialState> => {
    const username = formData.get("username");
    const password = formData.get("password");
    let error = { username: "", password: "" };

    if (!username?.toString().trim()) {
      error = {
        ...error,
        username: "Username can not be blank!",
      };
    } else {
      error = {
        ...error,
        username: "",
      };
    }
    if (!password?.toString().trim()) {
      error = { ...error, password: "Password can not be empty" };
    } else {
      error = {
        ...error,
        password: "",
      };
    }

    if (error.username || error.password) {
      return {
        success: false,
        error,
        values: {
          username: username?.toString() || "",
          password: password?.toString() || "",
        },
      };
    }

    try {
      await login(username!.toString(), password!.toString());
      toast.success("Logged in!");
      navigate("/user");
      return {
        success: true,
        error: { username: "", password: "" },
        values: { username: "", password: "" },
      };
    } catch (error) {
      console.log("Unable to login", error);
      toast.error(`Unable to login! ${error}`);
      return {
        ...prevState,
        success: false,
        values: {
          username: username?.toString() || "",
          password: password?.toString() || "",
        },
      };
    }
  };

  const [state, formAction, isPending] = useActionState(
    actionState,
    initialState,
  );

  return (
    <>
      {loading ? (
        <AiOutlineLoading3Quarters className="animate-spin" />
      ) : (
        <div className="flex bg-white/20 backdrop-blur-xl flex-col shadow-md w-120 rounded h-fit p-15 items-center justify-center">
          <h1 className="mb-8 text-2xl">LOGIN</h1>

          <div className="[&_input]:mb-5 mb-5 pb-5 border-b border-b-gray-500">
            <form
              action={formAction}
              autoComplete="off"
              className="flex flex-col items-center"
            >
              <Input
                type="text"
                id="username"
                name="username"
                placeholder="Username"
                className={`${state.error.username.length > 0 ? "outline-2 outline-red-400" : "outline-2 outline-transparent"}`}
                defaultValue={state.values.username}
              />
              <Input
                type="password"
                id="password"
                name="password"
                placeholder="Password"
                className={`${state.error.password.length > 0 ? "outline-2 outline-red-400" : "outline-2 outline-transparent"}`}
              />
              <button
                type="submit"
                disabled={isPending}
                className="rounded flex gap-2 px-4 py-2 shadow hover:shadow-xl active:shadow-lg cursor-pointer bg-white/50 backdrop-blur-3xl disabled:opacity-65 disabled:hover:shadow disabled:cursor-not-allowed hover:backdrop-blur-lg hover:bg-white/20"
              >
                {isPending ? (
                  <>
                    <VscLoading className="animate-spin text-2xl" /> Logging
                    in...{" "}
                  </>
                ) : (
                  "Login"
                )}
              </button>
            </form>
          </div>
          <button
            type="submit"
            disabled={isPending}
            onClick={() => window.location.href = "http://localhost:8000/api/auth/login/google"}
            className="rounded flex gap-2 px-4 py-2 shadow hover:shadow-xl active:shadow-lg cursor-pointer bg-white/50 backdrop-blur-3xl disabled:opacity-65 disabled:hover:shadow disabled:cursor-not-allowed hover:backdrop-blur-lg hover:bg-white/20 items-center"
          >
           <FaGoogle className="text-xl me-2"/> Login with google
          </button>
        </div>
      )}
    </>
  );
};

export default LoginPage;
