# secuencial.py

def propagate(self, typeinfer):
    """
    Ejecuta todas las restricciones. Captura y almacena errores,
    lo que permite seguir avanzando incluso si fallan algunas restricciones.
    """
    errors = []
    for constraint in self.constraints:
        loc = constraint.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename, lineno=loc.line):
            try:
                constraint(typeinfer)
            except ForceLiteralArg as e:
                errors.append(e)
            except TypingError as e:
                _logger.debug('captured error', exc_info=e)
                new_exc = TypingError(str(e), loc=constraint.loc, highlighting=False)
                errors.append(utils.chain_exception(new_exc, e))
            except Exception as e:
                if utils.use_old_style_errors():
                    _logger.debug('captured error', exc_info=e)
                    msg = 'Internal error at {con}.\n{err}\nEnable logging at debug level for details.'
                    new_exc = TypingError(msg.format(con=constraint, err=str(e)), loc=constraint.loc, highlighting=False)
                    errors.append(utils.chain_exception(new_exc, e))
                elif utils.use_new_style_errors():
                    raise e
                else:
                    msg = f"Unknown CAPTURED_ERRORS style: '{config.CAPTURED_ERRORS}'."
                    assert 0, msg
    return errors
