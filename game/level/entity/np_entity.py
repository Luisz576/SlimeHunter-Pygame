from game.level.entity import Entity


class NPEntity(Entity):
    def __init__(self, pos, group, collision_group, animations, start_animation_name):
        super().__init__(pos, group, collision_group, animations, start_animation_name)
        self.__goals = []

    def _register_goal(self, goal):
        self.__goals.append(goal)

    def _update_goals(self, delta):
        for goal in self.__goals:
            goal.update(delta)

    def update(self, delta):
        self._update_goals(delta)
        super().update(delta)
