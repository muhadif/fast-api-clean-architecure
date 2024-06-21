data "external_schema" "sqlalchemy" {
  program = [
    "atlas-provider-sqlalchemy",
     "--path", "./app/model",
    "--dialect", "mysql"
  ]
}

env "sqlalchemy" {
  src = data.external_schema.sqlalchemy.url
  dev = "mysql://fastapi:fastapi@localhost:3309/fastapi"
  migration {
    dir = "file://migrations"
  }
  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}