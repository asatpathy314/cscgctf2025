<?php

if($_SESSION["admin"] === false){
    return "You're not welcome. This part is only for canteen workers.";
}


class AdminModel {
    public $filename;
    public $logcontent;

    public function __construct($filename, $content) {
        $this->filename = $filename;
        $this->logcontent = $content;
        file_put_contents($filename, $content, FILE_APPEND);
    }

    public function __wakeup() {
        new LogFile($this->filename, $this->logcontent);
    }

    public static function read_logs($log) {
        $contents = file_get_contents($log);
        return $contents;
    }
}

class LogFile {
    public function __construct($filename, $content) {
        file_put_contents($filename, $content, FILE_APPEND);
    }
}
