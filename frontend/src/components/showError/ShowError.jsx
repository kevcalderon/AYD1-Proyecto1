import { Alert, AlertTitle } from "@mui/material";

const ShowError = ({ title, description, message }) => {
  return (
    <div className="w-4/5 flex flex-col align-items-center justify-center mx-auto">
      <Alert severity="error">
        <AlertTitle>{title}</AlertTitle>
        {description} — <strong>{message}</strong>
      </Alert>
    </div>
  );
};

export default ShowError;
