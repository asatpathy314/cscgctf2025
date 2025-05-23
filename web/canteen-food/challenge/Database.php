<?php
class Database {

    private static $db;
    private $connection;

    private function __construct() {
        $this->connection = new MySQLi('127.0.0.1', $_SERVER['DB_USER'], $_SERVER['DB_PASS'], $_SERVER['DB_NAME']);
    }

    function __destruct() {
        $this->connection->close();
    }

    public static function getConnection() {
        if (self::$db == null) {
            self::$db = new Database();
        }
        return self::$db->connection;
    }
}