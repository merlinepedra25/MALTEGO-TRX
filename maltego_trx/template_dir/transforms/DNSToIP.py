import socket

from maltego_trx.entities import IPAddress, DNS
from maltego_trx.maltego import MaltegoRequest, MaltegoResponse, CleanMaltegoEntity, UiMessage
from maltego_trx.server import registry
from maltego_trx.transform import DiscoverableTransform


@registry.register(display_name="DNS To IP", input_entity=DNS, description="Resolves a DNS name to a Host locally")
class DNSToIP(DiscoverableTransform):
    """
    Receive DNS name from the client, and resolve to IP address.
    """

    @classmethod
    def create_entities(cls, request: MaltegoRequest, response: MaltegoResponse):
        dns_name = request.value

        try:
            ip_address = socket.gethostbyname(dns_name)
            response.entities.append(CleanMaltegoEntity(IPAddress, ip_address))

        except socket.error as e:
            response.ui_messages.append(UiMessage("Error: " + str(e), 'PartialError'))

        # Write the slider value as a UI message - just for fun
        response.ui_messages.append(UiMessage("Slider value is at: " + str(request.slider), 'Inform'))
