# propagate_parallel.py

import ray
import logging
from numba.core.errors import TypingError, ForceLiteralArg
from numba.core import config, utils
import warnings
_logger = logging.getLogger(__name__)

@ray.remote
def propagate_parallel_func_0(remote_list_0, typeinfer):
    rtLst = []
    errors = []
    for loopIdx in range(len(remote_list_0)):
        constraint = remote_list_0[loopIdx]
        loc = constraint.loc
        with warnings.catch_warnings():
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
        rtLst.append(())
    return errors

def propagate_parallel(self, typeinfer):
    """
    Ejecuta en paralelo todas las restricciones de `self.constraints` usando Ray.
    """
    ray.init(ignore_reinit_error=True)

    remote_list_0 = list(self.constraints)
    totalLength = len(remote_list_0)
    BlockLength = totalLength // 10 or 1  # Evitar división por cero

    # Dividir en bloques de trabajo
    remote_list_1 = [
        propagate_parallel_func_0.remote(remote_list_0[i * BlockLength:(i + 1) * BlockLength], typeinfer)
        for i in range((totalLength + BlockLength - 1) // BlockLength)
    ]

    rmtTmp = ray.get(remote_list_1)

    # Combinar errores de todos los bloques
    errors = []
    for block_errors in rmtTmp:
        errors.extend(block_errors)

    return errors
