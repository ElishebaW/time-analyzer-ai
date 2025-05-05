package com.snake.game.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import com.snake.game.entity.Task;
import org.springframework.stereotype.Repository;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {
}