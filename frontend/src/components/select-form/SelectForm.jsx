import { TextField } from "@mui/material";
import { Controller } from "react-hook-form";

const SelectForm = ({
  control,
  required,
  errors,
  register,
  name,
  label,
  children,
  props,
  defaultValue,
}) => {
  return (
    <Controller
      control={control}
      defaultValue={defaultValue}
      name={name}
      render={({ field, fieldState }) => (
        <TextField
          select
          label={label}
          className="w-full"
          required={required}
          error={!!errors[name]}
          sx={{ display: "flex" }}
          helperText={fieldState.error ? errors[name].message : ""}
          {...register(name)}
          {...field}
          {...props}
        >
          {children}
        </TextField>
      )}
    />
  );
};

export default SelectForm;
