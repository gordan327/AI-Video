from abc import ABC, abstractmethod


class BaseRenderer(ABC):
    """所有隱私呈現方式的共同介面。"""

    @abstractmethod
    def render(
        self,
        frame,
        box: tuple[int, int, int, int],
    ):
        """對指定矩形區域進行隱私處理。"""

        raise NotImplementedError