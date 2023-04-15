import { Autocomplete, TextField } from "@mui/material";
import { Box } from "@mui/system";
import { Controller } from "react-hook-form";

const AutoCompleteForm = ({
  control,
  options,
  getOptionLabel,
  isOptionEqualToValue,
  renderOptions,
  getKey,
  errors,
  name,
  label,
  classname = "",
  rules,
  ...rest
}) => {
  return (
    <Controller
      control={control}
      name={name}
      defaultValue=""
      render={({ field, fieldState }) => (
        <span>
          <Autocomplete
            {...rest}
            className={classname}
            size="small"
            options={options}
            getOptionLabel={(option) => getOptionLabel(option)}
            isOptionEqualToValue={(option, value) =>
              isOptionEqualToValue(option, value)
            }
            filterSelectedOptions
            renderOption={(props, option) => (
              <Box component="li" {...props} key={getKey(option)}>
                {renderOptions(option)}
              </Box>
            )}
            renderInput={(params) => (
              <TextField {...params} label={label} required />
            )}
            onChange={(e, newValue) => field.onChange(newValue)}
          />
          {fieldState.error ? (
            <small className="text-red-500">{errors[name].message}</small>
          ) : null}
        </span>
      )}
    />
  );
};

export default AutoCompleteForm;
