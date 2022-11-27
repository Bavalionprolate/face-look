-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: db
-- Время создания: Ноя 26 2022 г., 03:29
-- Версия сервера: 10.9.3-MariaDB-1:10.9.3+maria~ubu2204
-- Версия PHP: 8.0.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `19261_face_look`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Photo_user`
--

CREATE TABLE `Photo_user` (
  `User_id` int(11) NOT NULL,
  `photo` longblob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `Photo_user`
--

INSERT INTO `Photo_user` (`User_id`, `photo`) VALUES
(1, 0x6466),
(1, NULL),
(1, NULL),
(1, NULL),
(1, NULL),
(1, NULL),
(1, 0x473a666163652d6c6f6f6b494d475f32303232313132365f3130343332372e6a7067);

-- --------------------------------------------------------

--
-- Структура таблицы `Prava`
--

CREATE TABLE `Prava` (
  `User_id` int(11) NOT NULL,
  `is_admin` bit(1) DEFAULT NULL,
  `is_programm_user` bit(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `User`
--

CREATE TABLE `User` (
  `id` int(11) NOT NULL,
  `login` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `fio` varchar(100) DEFAULT NULL,
  `pol` varchar(45) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `address` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `User`
--

INSERT INTO `User` (`id`, `login`, `password`, `fio`, `pol`, `birthday`, `address`) VALUES
(1, 'bavalion', '34781', 'Громыко Иван Александрович', 'Мужской', '2003-03-27', 'г.Иркутск, р.п. Маркова');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Photo_user`
--
ALTER TABLE `Photo_user`
  ADD KEY `fk_Photo_user_User1_idx` (`User_id`);

--
-- Индексы таблицы `Prava`
--
ALTER TABLE `Prava`
  ADD KEY `fk_Prava_User_idx` (`User_id`);

--
-- Индексы таблицы `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`id`);

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Photo_user`
--
ALTER TABLE `Photo_user`
  ADD CONSTRAINT `fk_Photo_user_User1` FOREIGN KEY (`User_id`) REFERENCES `User` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Ограничения внешнего ключа таблицы `Prava`
--
ALTER TABLE `Prava`
  ADD CONSTRAINT `fk_Prava_User` FOREIGN KEY (`User_id`) REFERENCES `User` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
