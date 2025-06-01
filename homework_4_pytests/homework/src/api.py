#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import hashlib
import json
import logging
import uuid
from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, HTTPServer

from src.exceptions import ValidationException
from src.scoring import get_interests, get_score

SALT = "Otus"
ADMIN_LOGIN = "admin"
ADMIN_SALT = "42"
OK = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404
INVALID_REQUEST = 422
INTERNAL_ERROR = 500
ERRORS = {
    BAD_REQUEST: "Bad Request",
    FORBIDDEN: "Forbidden",
    NOT_FOUND: "Not Found",
    INVALID_REQUEST: "Invalid Request",
    INTERNAL_ERROR: "Internal Server Error",
}
UNKNOWN = 0
MALE = 1
FEMALE = 2
GENDERS = {
    UNKNOWN: "unknown",
    MALE: "male",
    FEMALE: "female",
}


class Field:
    def __init__(self, required=False, nullable=False):
        self.required = required
        self.nullable = nullable

    def validate(self, value):
        if value in ("", None, [], {}):
            if self.required and not self.nullable:
                raise ValidationException(
                    message="Field is required",
                    field=self.__class__.__name__,
                    value=value,
                    hint="Field cannot be None",
                )
            return


class MetaRequest(type):
    def __new__(cls, name, bases, attrs):
        fields = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value
        attrs['__fields__'] = fields

        return super().__new__(cls, name, bases, attrs)


class CharField(Field):
    def validate(self, value):
        super().validate(value)

        if not isinstance(value, str):
            raise ValidationException(
                message="Field must be a string",
                field=self.__class__.__name__,
                value=value,
                hint="Field must be a string",
            )



class ArgumentsField(Field):

    def validate(self, value):
        super().validate(value)
        if not isinstance(value, dict):
            raise ValidationException(
                message="Field must be a dictionary",
                field=self.__class__.__name__,
                value=value,
                hint="Field must be a dictionary",
            )


class EmailField(Field):
    def validate(self, value):
        super().validate(value)

        if '@' not in value:
            raise ValidationException(
                message="Invalid email format",
                field=self.__class__.__name__,
                value=value,
                hint="Email must contain '@'",
            )


class PhoneField(Field):
    def validate(self, value):
        super().validate(value)

        if isinstance(value, int):
            value = str(value)
        if len(value) != 11:
            raise ValidationException(
                message="Invalid phone number format",
                field=self.__class__.__name__,
                value=value,
                hint="Phone number must be 11 digits",
            )
        if not value.startswith("7"):
            raise ValidationException(
                message="Invalid phone number format",
                field=self.__class__.__name__,
                value=value,
                hint="Phone number must start with '7'",
            )


class DateField(Field):
    def validate(self, value):
        super().validate(value)

        if isinstance(value, str):
            try:
                value = datetime.datetime.strptime(value, "%d.%m.%Y").date()
            except ValueError:
                raise ValidationException(
                    message="Invalid date format",
                    field=self.__class__.__name__,
                    value=value,
                    hint="Date must be in 'dd.mm.yyyy' format",
                )
        else:
            raise ValidationException(
                message="Invalid date format",
                field=self.__class__.__name__,
                value=value,
                hint="Date must be a string",
            )


class BirthDayField(Field):
    def validate(self, value):
        super().validate(value)

        try:
            birthday = datetime.datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValidationException(
                message="Invalid date format",
                field=self.__class__.__name__,
                value=value,
                hint="Date must be in 'dd.mm.yyyy' format",
            )
        today = datetime.date.today()
        if (today - birthday).days > 70 * 365.25:
            raise ValidationException(
                message="Invalid date of birth",
                field=self.__class__.__name__,
                value=value,
                hint="Date of birth must be less than 70 years ago",
            )


class GenderField(Field):
    def validate(self, value):
        super().validate(value)
        if not isinstance(value, int):
            raise ValidationException(
                message="Invalid gender format",
                field=self.__class__.__name__,
                value=value,
                hint="Gender value must be a digit",
            )

        if value not in (0, 1, 2):
            raise ValidationException(
                message="Invalid gender value",
                field=self.__class__.__name__,
                value=value,
                hint="Gender must be 0, 1, or 2",
            )


class ClientIDsField(Field):
    def validate(self, value):
        super().validate(value)
        if not isinstance(value, list):
            raise ValidationException(
                message="Invalid client IDs format",
                field=self.__class__.__name__,
                value=value,
                hint="Client IDs must be a list",
            )
        if not all(isinstance(i, int) for i in value):
            raise ValidationException(
                message="Invalid client ID format",
                field=self.__class__.__name__,
                value=value,
                hint="Client IDs must be integers",
            )


class BaseRequest(metaclass=MetaRequest):
    def __init__(self, **kwargs):
        for name, field in self.__fields__.items():
            if name in kwargs:
                value = kwargs[name]
                field.validate(value)
                setattr(self, name, value)
            elif field.required:
                raise ValidationException(
                    message=f"Missing required field",
                    field=name,
                    value=None,
                    hint="This field is required and was not provided"
                )
            else:
                setattr(self, name, None)



class ClientsInterestsRequest(BaseRequest):
    client_ids = ClientIDsField(required=True)
    date = DateField(required=False, nullable=True)


class OnlineScoreRequest(BaseRequest):
    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)

    def has_valid_pair(self):
        if any(
                [
                    (self.phone and self.email) or
                    (self.first_name and self.last_name) or
                    (self.birthday and self.gender is not None)
                ]
        ):
            return True
        return False

    def validate(self):
        if self.has_valid_pair() is False:
            raise ValidationException(
                message="No valid pair of fields",
                field="phone, email, first_name, last_name, birthday, gender",
                value=[
                    self.phone,
                    self.email,
                    self.first_name,
                    self.last_name,
                    self.birthday,
                    self.gender
                ],
            )


class MethodRequest(BaseRequest):
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=False)

    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN


def check_auth(request):
    if request.is_admin:
        digest = hashlib.sha512(
            (datetime.datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT).encode('utf-8')
        ).hexdigest()
    else:
        digest = hashlib.sha512(
            (request.account + request.login + SALT).encode('utf-8')
        ).hexdigest()
    return digest == request.token


def method_handler(request, ctx, store):
    request_body = request.get('body')
    try:
        request_method = MethodRequest(
            account=request_body.get('account'),
            login=request_body.get('login'),
            token=request_body.get('token'),
            method=request_body.get('method'),
            arguments=request_body.get('arguments'),
        )
    except ValidationException as e:
        return {"error": str(e)}, INVALID_REQUEST


    if check_auth(request_method):
        args = request_body.get('arguments', {})
        valid_args = {k: v for k, v in args.items() if v is not None}
        ctx["has"] = [k for k, v in args.items() if v not in (None, "", [])]
        if request_method.is_admin:
            return {
                "score": 42,
            }, OK
        if request_body.get('method') == "online_score":
            try:
                online_score_request = OnlineScoreRequest(**valid_args)
                online_score_request.validate()
                score = get_score(
                    store=store,
                    phone=online_score_request.phone,
                    email=online_score_request.email,
                    birthday=online_score_request.birthday,
                    gender=online_score_request.gender,
                    first_name=online_score_request.first_name,
                    last_name=online_score_request.last_name,
                )
            except ValidationException as e:
                return {"error": str(e)}, INVALID_REQUEST

            return {"score": score}, OK

        elif request_body.get('method') == "clients_interests":
            try:
                client_ids_request = ClientsInterestsRequest(**valid_args)
            except ValidationException as e:
                return {"error": str(e)}, INVALID_REQUEST

            ctx["nclients"] = len(client_ids_request.client_ids)

            client_interests = {}

            for client_id in client_ids_request.client_ids:
                client_interests[client_id] = get_interests(
                    store=store,
                    cid=client_id,
                )

            return client_interests, OK

    return {"error": "Forbidden"}, 403


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "method": method_handler
    }
    store = None

    def get_request_id(self, headers):
        return headers.get('HTTP_X_REQUEST_ID', uuid.uuid4().hex)

    def do_POST(self):
        response, code = {}, OK
        context = {"request_id": self.get_request_id(self.headers)}
        request = None
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            request = json.loads(data_string)
        except:
            code = BAD_REQUEST

        if request:
            path = self.path.strip("/")
            logging.info("%s: %s %s" % (self.path, data_string, context["request_id"]))
            if path in self.router:
                try:
                    response, code = self.router[path](
                        {"body": request, "headers": self.headers},
                        context,
                        self.store,
                    )
                except Exception as e:
                    logging.exception("Unexpected error: %s" % e)
                    code = INTERNAL_ERROR
            else:
                code = NOT_FOUND

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if code not in ERRORS:
            r = {"response": response, "code": code}
        else:
            r = {
                "error": response or ERRORS.get(code, "Unknown Error"),
                "code": code
            }
        context.update(r)
        logging.info(context)
        self.wfile.write(json.dumps(r).encode('utf-8'))
        return


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", action="store", type=int, default=8080)
    parser.add_argument("-l", "--log", action="store", default=None)
    args = parser.parse_args()
    logging.basicConfig(
        filename=args.log,
        level=logging.INFO,
        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S'
    )
    server = HTTPServer(("localhost", args.port), MainHTTPHandler)
    logging.info("Starting server at %s" % args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
