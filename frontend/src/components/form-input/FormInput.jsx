import { FloatingLabel } from "react-bootstrap";
import Form from "react-bootstrap/Form";

const FormInput = ({
  placeholder,
  errors,
  name,
  controlId,
  register,
  type,
  props = null,
  required = false,
}) => {
  return (
    <Form.Group className="w-100" controlId={controlId}>
      <FloatingLabel controlId={controlId} label={placeholder} className="mb-2">
        <Form.Control
          type={type}
          placeholder={placeholder}
          {...register(name)}
          defaultValue=""
          {...props}
          isInvalid={!!errors[name]}
          size="sm"
          required={required}
        />
      </FloatingLabel>
      {!!errors[name] && (
        <Form.Text className="text-danger">{errors[name].message}</Form.Text>
      )}
    </Form.Group>
  );
};

export default FormInput;
